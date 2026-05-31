#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <std_srvs/srv/empty.hpp>

class PatrolController : public rclcpp::Node
{
public:
  PatrolController()
  : Node("patrol_controller"), is_running_(true)
  {
    // Declare parameters with default values
    this->declare_parameter("linear_speed", 1.5);
    this->declare_parameter("angular_speed", 1.0);

    // Get initial parameter values
    linear_speed_ = this->get_parameter("linear_speed").as_double();
    angular_speed_ = this->get_parameter("angular_speed").as_double();

    // Publisher for turtle velocity commands
    cmd_vel_pub_ = this->create_publisher<geometry_msgs::msg::Twist>(
      "/turtle1/cmd_vel", 10);

    // Timer to publish velocity commands at 10 Hz
    timer_ = this->create_wall_timer(
      std::chrono::milliseconds(100),
      std::bind(&PatrolController::timer_callback, this));

    // /stop service
    stop_service_ = this->create_service<std_srvs::srv::Empty>(
      "/stop",
      std::bind(&PatrolController::stop_callback, this,
                std::placeholders::_1, std::placeholders::_2));

    // /continue service
    continue_service_ = this->create_service<std_srvs::srv::Empty>(
      "/continue",
      std::bind(&PatrolController::continue_callback, this,
                std::placeholders::_1, std::placeholders::_2));

    // Parameter callback to handle runtime parameter changes
    param_callback_handle_ = this->add_on_set_parameters_callback(
      std::bind(&PatrolController::on_parameter_change, this, std::placeholders::_1));

    RCLCPP_INFO(this->get_logger(),
      "PatrolController started: linear=%.2f, angular=%.2f",
      linear_speed_, angular_speed_);
  }

private:
  void timer_callback()
  {
    // Re-read parameters each cycle (allows runtime changes)
    linear_speed_ = this->get_parameter("linear_speed").as_double();
    angular_speed_ = this->get_parameter("angular_speed").as_double();

    auto msg = geometry_msgs::msg::Twist();
    if (is_running_) {
      msg.linear.x = linear_speed_;
      msg.angular.z = angular_speed_;
    } else {
      msg.linear.x = 0.0;
      msg.angular.z = 0.0;
    }
    cmd_vel_pub_->publish(msg);
  }

  void stop_callback(
    const std::shared_ptr<std_srvs::srv::Empty::Request> /*request*/,
    std::shared_ptr<std_srvs::srv::Empty::Response> /*response*/)
  {
    is_running_ = false;
    RCLCPP_INFO(this->get_logger(), "Turtle STOPPED");
  }

  void continue_callback(
    const std::shared_ptr<std_srvs::srv::Empty::Request> /*request*/,
    std::shared_ptr<std_srvs::srv::Empty::Response> /*response*/)
  {
    is_running_ = true;
    RCLCPP_INFO(this->get_logger(), "Turtle RESUMED");
  }

  rcl_interfaces::msg::SetParametersResult on_parameter_change(
    const std::vector<rclcpp::Parameter> & parameters)
  {
    auto result = rcl_interfaces::msg::SetParametersResult();
    result.successful = true;
    for (const auto & param : parameters) {
      if (param.get_name() == "linear_speed") {
        linear_speed_ = param.as_double();
        RCLCPP_INFO(this->get_logger(), "linear_speed updated to %.2f", linear_speed_);
      } else if (param.get_name() == "angular_speed") {
        angular_speed_ = param.as_double();
        RCLCPP_INFO(this->get_logger(), "angular_speed updated to %.2f", angular_speed_);
      }
    }
    return result;
  }

  // Member variables
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr cmd_vel_pub_;
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Service<std_srvs::srv::Empty>::SharedPtr stop_service_;
  rclcpp::Service<std_srvs::srv::Empty>::SharedPtr continue_service_;
  rclcpp::node_interfaces::OnSetParametersCallbackHandle::SharedPtr param_callback_handle_;

  double linear_speed_;
  double angular_speed_;
  bool is_running_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<PatrolController>());
  rclcpp::shutdown();
  return 0;
}
