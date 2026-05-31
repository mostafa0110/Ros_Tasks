#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/int32.hpp"

using std::placeholders::_1;

class MySub : public rclcpp::Node {
public:
    MySub(): Node("MySub"){
        subscription_ = this->create_subscription<std_msgs::msg::Int32>(
      "myTopic", 10, std::bind(&MySub::topic_callback, this, _1));
    }

private:
    void topic_callback(const std_msgs::msg::Int32 & msg) const {
        RCLCPP_INFO(this->get_logger(), "I heard: '%d'", msg.data);
    }   
    rclcpp::Subscription<std_msgs::msg::Int32>::SharedPtr subscription_;
};

int main(int argc, char * argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MySub>());
  rclcpp::shutdown();
  return 0;
}