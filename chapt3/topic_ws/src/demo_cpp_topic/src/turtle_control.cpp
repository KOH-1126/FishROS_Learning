#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "turtlesim/msg/pose.hpp"
#include <chrono>

using namespace std::chrono_literals;

class TurtleControl:public rclcpp::Node
{
    private:
        rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_; //发布者的智能指针
        rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr subscription_; //订阅者的智能指针
        double target_x_{1.0}; //目标位置的x坐标
        double target_y_{1.0}; //目标位置的y坐标
        double P_{1.0}; //比例增益
        double max_linear_speed_{3.0}; //最大线速度

    public:
        explicit TurtleControl(const std::string& node_name):Node(node_name)
        {
            publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("turtle1/cmd_vel", 10); 
            subscription_ = this->create_subscription<turtlesim::msg::Pose>(
                "turtle1/pose", 10, std::bind(&TurtleControl::on_pose_received, this, 
                    std::placeholders::_1));
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