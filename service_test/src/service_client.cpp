#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

using namespace std::chrono_literals;

class AddTwoIntsClient : public rclcpp::Node
{
public:
  AddTwoIntsClient() : Node("add_two_ints_client")
  {
    client_ = this->create_client<example_interfaces::srv::AddTwoInts>("add_two_ints");
    send_request();
  }

private:
  void send_request()
  {
    auto request = std::make_shared<example_interfaces::srv::AddTwoInts::Request>();
    request->a = 1;
    request->b = 2;
    if (!client_->wait_for_service(1s)) {
      RCLCPP_INFO(this->get_logger(), "Service not available");
      return;}

    // Send the request asynchronously
    auto result_future = client_->async_send_request(request, 
        [this](rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedFuture future) {
            auto response = future.get();
            RCLCPP_INFO(this->get_logger(), "Result: %ld", response->sum);
        }
    );
    if (rclcpp::spin_until_future_complete(this->get_node_base_interface(), result_future) ==
        rclcpp::FutureReturnCode::SUCCESS)
    {
      RCLCPP_INFO(this->get_logger(), "Result of add_two_ints: %ld", result_future.get()->sum);
    } else {
      RCLCPP_ERROR(this->get_logger(), "Failed to call service add_two_ints");
    }
  }

  rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedPtr client_;
};


int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<AddTwoIntsClient>();
  rclcpp::spin(node);
  rclcpp::shutdown();
}