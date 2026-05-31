#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"

#include <chrono>
#include <functional>
#include <memory>
#include <string>


using namespace std::chrono_literals;

class VelocityLimiter : public rclcpp::Node {

public:
    VelocityLimiter(): Node("VelocityLimiter")  {
        subscription_ = this->create_subscription<geometry_msgs::msg::Twist>(
        "cmd_vel", 10, std::bind(&VelocityLimiter::teleop_callback, this,std::placeholders::_1));

        publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("cmd_vel_limited",10);

    }



private:
    void teleop_callback(const geometry_msgs::msg::Twist::SharedPtr msg) {
        RCLCPP_INFO(this->get_logger(), "Received velocity command: linear=%f, angular=%f", msg->linear.x, msg->angular.z);
        last_msg_ = *msg;
        if(last_msg_.linear.x > 1.0  ) {
            last_msg_.linear.x = 1.0;
        }
        else if(last_msg_.linear.x < -1.0) {
            last_msg_.linear.x = -1.0;
        }
        if(last_msg_.angular.z > 1.5) {
            last_msg_.angular.z = 1.5;
        }
        else if(last_msg_.angular.z < -1.5) {
            last_msg_.angular.z = -1.5;
        }
        publisher_->publish(last_msg_);
        RCLCPP_INFO(this->get_logger(), "Published limited velocity command: linear=%f, angular=%f", last_msg_.linear.x, last_msg_.angular.z);
    }


    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
    rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr subscription_;
    geometry_msgs::msg::Twist last_msg_;
};

int main(int argc, char * argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<VelocityLimiter>());
  rclcpp::shutdown();
  return 0;
}
