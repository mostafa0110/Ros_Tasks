#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/int32.hpp"

#include <chrono>
#include <functional>
#include <memory>
#include <string>
#include <fstream>

using namespace std::chrono_literals;

class MyPub : public rclcpp::Node {

public:
    MyPub(): Node("MyPub")  , count_(0){
        file.open("/sys/class/thermal/thermal_zone0/temp");
        publisher_ = this->create_publisher<std_msgs::msg::Int32>("myTopic",10);
        timer_ = this->create_wall_timer(
        1000ms, std::bind(&MyPub::timer_callback, this));
    }



private:
    void timer_callback() {
        auto message = std_msgs::msg::Int32();
        if(file.is_open()){
            file >> count_;
            file.seekg(0);
            count_ = count_ / 1000;
        }
        message.data = count_;
        RCLCPP_INFO(this->get_logger(), "CPU Temperature: '%d'", message.data);
        publisher_->publish(message);
    }


    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<std_msgs::msg::Int32>::SharedPtr publisher_;
    size_t count_;
    std::ifstream file;
};

int main(int argc, char * argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MyPub>());
  rclcpp::shutdown();
  return 0;
}
