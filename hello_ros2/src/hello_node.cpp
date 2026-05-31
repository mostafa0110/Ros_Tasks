#include "rclcpp/rclcpp.hpp"

class HelloNode : public rclcpp::Node {
public:
  HelloNode() : Node("hello_node_cpp") {
    RCLCPP_INFO(this->get_logger(), "Hello, ROS 2 Jazzy!");
  }
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<HelloNode>());
  rclcpp::shutdown();
  return 0;
}