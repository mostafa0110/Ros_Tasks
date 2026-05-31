#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

class AddTwoInts : public rclcpp::Node
{
public:
  AddTwoInts() : Node("add_two_ints")
  {
    service_ = this->create_service<example_interfaces::srv::AddTwoInts>(
        "add_two_ints", std::bind(&AddTwoInts::handle_add_two_ints, this, std::placeholders::_1, std::placeholders::_2));
  } 
private:
  void handle_add_two_ints(const std::shared_ptr<example_interfaces::srv::AddTwoInts::Request> request,
                           std::shared_ptr<example_interfaces::srv::AddTwoInts::Response> response)
  {    response->sum = request->a + request->b;
    RCLCPP_INFO(this->get_logger(), "Incoming request\na: %ld b: %ld sum: %ld",
                request->a, request->b, response->sum);
  }
  rclcpp::Service<example_interfaces::srv::AddTwoInts>::SharedPtr service_;
};


int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<AddTwoInts>();
  rclcpp::spin(node);
  rclcpp::shutdown();
}