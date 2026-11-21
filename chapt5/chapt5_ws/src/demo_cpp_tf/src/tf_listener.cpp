#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "tf2/LinearMath/Quaternion.h"
#include "tf2_geometry_msgs/tf2_geometry_msgs.hpp"
#include "tf2_ros/transform_listener.h"
#include "tf2_ros/buffer.h"
#include "tf2/utils.h"
#include <chrono>

using namespace std::chrono_literals;

class TFListener : public rclcpp::Node
{
    private:
        std::shared_ptr<tf2_ros::TransformListener> listener_;
        rclcpp::TimerBase::SharedPtr timer_;
        std::shared_ptr<tf2_ros::Buffer> buffer_;
    public:
        TFListener() : Node("tf_listener")
        {
            this->buffer_ = std::make_shared<tf2_ros::Buffer>(this->get_clock());
            this->listener_ = std::make_shared<tf2_ros::TransformListener>(*buffer_, this);
            timer_ = this->create_wall_timer(
                1s,
                std::bind(&TFListener::getTransform, this)
            );
        }

        void getTransform()
        {
            try
            {
                const auto transform = buffer_->lookupTransform("base_link", "target_point", 
                    this->get_clock()->now(), rclcpp::Duration::from_seconds(1.0f));

                auto translation = transform.transform.translation;
                auto rotation = transform.transform.rotation;
                double y, p, r;
                tf2::getEulerYPR(rotation, y, p, r);
                RCLCPP_INFO(this->get_logger(), "Translation: x=%.2f, y=%.2f, z=%.2f", translation.x, translation.y, translation.z);
                RCLCPP_INFO(this->get_logger(), "Rotation: yaw=%.2f, pitch=%.2f, roll=%.2f", y, p, r);
            }
            catch(const std::exception& e)
            {
                RCLCPP_WARN(this->get_logger(), "Could not get transform: %s", e.what());
            }
        }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TFListener>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}