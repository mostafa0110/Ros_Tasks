#include "rclcpp/rclcpp.hpp"
#include "nav_msgs/msg/odometry.hpp"

#include <chrono>
#include <memory>
#include <string>

using namespace std::chrono_literals;

class SyntheticOdometry : public rclcpp::Node {
public:
    SyntheticOdometry() : Node("SyntheticOdometry") {
        publisher_ = this->create_publisher<nav_msgs::msg::Odometry>("odom", 10);
        timer_ = this->create_wall_timer(
        1000ms, std::bind(&SyntheticOdometry::timer_callback, this));  // 10 Hz
    }
private:
    void timer_callback() {
        count_ += 0.1; 
        auto message = nav_msgs::msg::Odometry();
        message.header.stamp = this->get_clock()->now();
        message.header.frame_id = "odom";
        message.child_frame_id = "base_link";
        message.pose.pose.position.x = count_;
        message.pose.pose.position.y = 0.0;
        message.pose.pose.position.z = 0.0;
        message.pose.pose.orientation.x = 0.0;
        message.pose.pose.orientation.y = 0.0;
        message.pose.pose.orientation.z = 0.0;
        message.pose.pose.orientation.w = 1.0;
        message.twist.twist.linear.x = 0.1;
        publisher_->publish(message);
    }
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<nav_msgs::msg::Odometry>::SharedPtr publisher_;
    double count_ = 0;
};


int main(int argc, char * argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<SyntheticOdometry>());
  rclcpp::shutdown();
  return 0;
}