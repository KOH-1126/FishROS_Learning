#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "turtlesim/msg/pose.hpp"
#include "chapt4_interfaces/srv/patrol.hpp"
#include "rcl_interfaces/msg/set_parameters_result.hpp"


using namespace std::chrono_literals;
using Patrol = chapt4_interfaces::srv::Patrol;
using SetParametersResult = rcl_interfaces::msg::SetParametersResult;

class TurtleControl:public rclcpp::Node
{
    private:
        OnSetParametersCallbackHandle::SharedPtr param_callback_handle_; //参数回调句柄
        rclcpp::Service<Patrol>::SharedPtr patrol_service_; //服务的智能指针
        rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_; //发布者的智能指针
        rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr subscription_; //订阅者的智能指针
        double target_x_{1.0}; //目标位置的x坐标
        double target_y_{1.0}; //目标位置的y坐标
        double P_{1.0}; //比例增益
        double max_linear_speed_{3.0}; //最大线速度

    public:
        explicit TurtleControl(const std::string& node_name):Node(node_name)
        {
            this->declare_parameter<double>("P", 1.0);
            this->declare_parameter<double>("max_linear_speed", 3.0);
            this->get_parameter("P", P_);
            this->get_parameter("max_linear_speed", max_linear_speed_);
            param_callback_handle_ = this->add_on_set_parameters_callback( 
                [&](const std::vector<rclcpp::Parameter> & parameters) -> SetParametersResult {
                    SetParametersResult result;
                    result.reason = "";
                    result.successful = true;
                    for(const auto & parameter: parameters)
                    {
                        if(parameter.get_name() == "P")
                        {
                            P_ = parameter.as_double();
                            RCLCPP_INFO(this->get_logger(), "Updated P to %.2f", P_);
                        }
                        else if(parameter.get_name() == "max_linear_speed")
                        {
                            max_linear_speed_ = parameter.as_double();
                            RCLCPP_INFO(this->get_logger(), "Updated max_linear_speed to %.2f", max_linear_speed_);
                        }
                    }
                    return result;
                }
            );
            patrol_service_ = this->create_service<Patrol>("patrol", [&](const Patrol::Request::SharedPtr request,
            Patrol::Response::SharedPtr response) -> void {
                if(
                    (0<request->target_x && request->target_x<11.0f) &&
                    (0<request->target_y && request->target_y<11.0f)
                )
                {
                    target_x_ = request->target_x;
                    target_y_ = request->target_y;
                    response->result = Patrol::Response::SUCCESS;
                }
                else
                {
                    response->result = Patrol::Response::FAILURE;
                }
            } );
            publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("turtle1/cmd_vel", 10); // 发布目标位置和姿态
            subscription_ = this->create_subscription<turtlesim::msg::Pose>(
                "turtle1/pose", 10, std::bind(&TurtleControl::on_pose_received, this, 
                    std::placeholders::_1)); // 订阅乌龟的位姿信息作为反馈
        }

        void on_pose_received(const turtlesim::msg::Pose::SharedPtr pose)
        {
            auto current_x = pose->x;
            auto current_y = pose->y;
            RCLCPP_INFO(this->get_logger(), "Current position: (%.2f, %.2f)", current_x, current_y);

            auto distance = std::sqrt(std::pow(target_x_ - current_x, 2) + std::pow(target_y_ - current_y, 2));
            auto err_angle = std::atan2(target_y_ - current_y, target_x_ - current_x) - pose->theta;

            auto msg = geometry_msgs::msg::Twist();
            if(distance > 0.1)
            {
                if(fabs(err_angle) > 0.1){
                    msg.angular.z = P_ * err_angle;
                }
                else{
                    msg.linear.x = P_ * distance;
                }
            }

            if(msg.linear.x > max_linear_speed_){
                msg.linear.x = max_linear_speed_;
            }

            publisher_->publish(msg);
        }

};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TurtleControl>("turtle_control");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}