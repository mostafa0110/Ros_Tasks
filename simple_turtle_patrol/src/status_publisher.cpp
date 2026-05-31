#include <rclcpp/rclcpp.hpp>
#include <turtlesim/msg/pose.hpp>
#include <simple_turtle_patrol/msg/robot_status.hpp>
#include <cmath>

class StatusPublisher : public rclcpp::Node
{
public:
  StatusPublisher()
  : Node("status_publisher"),
    state_("running"),
    temperature_(36.0f),
    lap_count_(0),
    cumulative_angle_(0.0),
    prev_theta_(0.0),
    first_pose_received_(false)
  {
    // Declare and get the status publishing rate parameter
    this->declare_parameter("status_rate", 5.0);
    double status_rate = this->get_parameter("status_rate").as_double();

    // Subscribe to turtle1/pose to get current turtle position
    pose_sub_ = this->create_subscription<turtlesim::msg::Pose>(
      "/turtle1/pose", 10,
      std::bind(&StatusPublisher::pose_callback, this, std::placeholders::_1));

    // Publisher for the custom RobotStatus message
    status_pub_ = this->create_publisher<simple_turtle_patrol::msg::RobotStatus>(
      "/robot/status", 10);

    // Timer to publish status at the configured rate
    int period_ms = static_cast<int>(1000.0 / status_rate);
    timer_ = this->create_wall_timer(
      std::chrono::milliseconds(period_ms),
      std::bind(&StatusPublisher::publish_status, this));

    RCLCPP_INFO(this->get_logger(),
      "StatusPublisher started at %.1f Hz", status_rate);
  }

private:
  void pose_callback(const turtlesim::msg::Pose::SharedPtr msg)
  {
    // Store current pose
    current_pose_ = *msg;

    // Track cumulative angle for lap counting
    if (!first_pose_received_) {
      prev_theta_ = msg->theta;
      first_pose_received_ = true;
      return;
    }

    // Calculate angle delta (handle wrap-around at ±π)
    double delta = msg->theta - prev_theta_;
    if (delta > M_PI) delta -= 2.0 * M_PI;
    if (delta < -M_PI) delta += 2.0 * M_PI;

    cumulative_angle_ += delta;
    prev_theta_ = msg->theta;

    // One full lap = 2π radians of cumulative rotation
    lap_count_ = static_cast<int>(std::abs(cumulative_angle_) / (2.0 * M_PI));

    // Determine state from linear velocity
    if (std::abs(msg->linear_velocity) < 0.01 &&
        std::abs(msg->angular_velocity) < 0.01) {
      state_ = "stopped";
    } else {
      state_ = "running";
    }

    // Dummy temperature: base 36 + a small contribution from speed
    temperature_ = 36.0f + static_cast<float>(msg->linear_velocity) * 0.5f;
  }

  void publish_status()
  {
    auto status_msg = simple_turtle_patrol::msg::RobotStatus();

    status_msg.pose.x = current_pose_.x;
    status_msg.pose.y = current_pose_.y;
    status_msg.pose.theta = current_pose_.theta;
    status_msg.state = state_;
    status_msg.temperature = temperature_;
    status_msg.lap_count = lap_count_;

    status_pub_->publish(status_msg);
  }

  // Subscribers & Publishers
  rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr pose_sub_;
  rclcpp::Publisher<simple_turtle_patrol::msg::RobotStatus>::SharedPtr status_pub_;
  rclcpp::TimerBase::SharedPtr timer_;

  // State
  turtlesim::msg::Pose current_pose_;
  std::string state_;
  float temperature_;
  int lap_count_;
  double cumulative_angle_;
  double prev_theta_;
  bool first_pose_received_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<StatusPublisher>());
  rclcpp::shutdown();
  return 0;
}
