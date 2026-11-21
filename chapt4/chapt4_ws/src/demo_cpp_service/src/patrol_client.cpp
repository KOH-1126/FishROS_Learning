#include "rclcpp/rclcpp.hpp"
#include "chapt4_interfaces/srv/patrol.hpp"
#include <chrono>
#include <ctime>
#include "rcl_interfaces/msg/parameter.hpp"
#include "rcl_interfaces/msg/parameter_value.hpp"
#include "rcl_interfaces/msg/parameter_type.hpp"
#include "rcl_interfaces/srv/set_parameters.hpp"

using namespace std::chrono_literals;
using Patrol = chapt4_interfaces::srv::Patrol;
using SetP = rcl_interfaces::srv::SetParameters;

class PatrolClient:public rclcpp::Node
{
    private:
        rclcpp::TimerBase::SharedPtr timer_; // 定时器的智能指针
        rclcpp::Client<Patrol>::SharedPtr client_; // 客户端的智能指针
    public:
        PatrolClient(const std::string& node_name):Node(node_name)
        {
            srand(time(nullptr));
            client_ = this->create_client<Patrol>("patrol");
            timer_ = this->create_wall_timer(10s, [&]()->void{
                // 检查服务是否可用
                while(!client_->wait_for_service(1s))
                {
                    if(!rclcpp::ok())
                    {
                        RCLCPP_ERROR(this->get_logger(), "Interrupted while waiting for the service. Exiting.");
                        return;
                    }
                    RCLCPP_INFO(this->get_logger(), "Service not available, waiting again...");
                }
                // 构造请求对象
                auto request = std::make_shared<Patrol::Request>();
                request->target_x = rand() % 15;
                request->target_y = rand() % 15;
                RCLCPP_INFO(this->get_logger(), "Sending request (randomly): target_x=%.2f, target_y=%.2f", request->target_x, request->target_y);
                // 发送请求
                client_->async_send_request(request, [&](rclcpp::Client<Patrol>::SharedFuture result_future)->void{
                    auto response = result_future.get(); 
                    if(response->result==Patrol::Response::SUCCESS){
                        RCLCPP_INFO(this->get_logger(), "Patrol succeeded!");
                    }
                    else if(response->result==Patrol::Response::FAILURE){
                        RCLCPP_INFO(this->get_logger(), "Patrol failed..");
                    }
                });
            });
        }
    
        /**
         * 创建客户端发送请求，返回结果
         */
        SetP::Response::SharedPtr call_set_parameter(const rcl_interfaces::msg::Parameter &param)
        {
            auto param_client = this->create_client<SetP>("/turtle_control/set_parameters");
            // 检查服务是否可用
            while(!param_client->wait_for_service(1s))
            {
                if(!rclcpp::ok())
                {
                    RCLCPP_ERROR(this->get_logger(), "Interrupted while waiting for the service. Exiting.");
                    return nullptr;
                }
                RCLCPP_INFO(this->get_logger(), "Service not available, waiting again...");
            }
            // 构造请求对象
            auto request = std::make_shared<SetP::Request>();
            request->parameters.push_back(param);
            // 发送请求
            auto future = param_client->async_send_request(request);
            rclcpp::spin_until_future_complete(this->get_node_base_interface(), future);
            auto reponse = future.get();
            return reponse;
        };
        

        /**
         * 更新参数K
         */
        void update_server_param_P(double P)
        {
            // 构造参数对象
            auto param = rcl_interfaces::msg::Parameter();
            param.name = "P";
            // 创建参数值
            auto param_value = rcl_interfaces::msg::ParameterValue();
            param_value.type = rcl_interfaces::msg::ParameterType::PARAMETER_DOUBLE;
            param_value.double_value = P;
            param.value = param_value;
            // 请求参数更新
            auto response = this->call_set_parameter(param);
            if(response == NULL){
                RCLCPP_ERROR(this->get_logger(), "Failed to call set_parameter service.");
                return;
            }
            for(auto result: response->results){
                if(result.successful){
                    RCLCPP_INFO(this->get_logger(), "Successfully updated parameter P to %.2f", P);
                }
                else{
                    RCLCPP_ERROR(this->get_logger(), "Failed to update parameter P: %s", result.reason.c_str());
                }
            }
        }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<PatrolClient>("patrol_client");
    node->update_server_param_P(4.0);
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}