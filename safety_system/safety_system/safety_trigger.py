import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from std_msgs.msg import String


class SafetyTrigger(Node):
    def __init__(self):
        super().__init__('safety_trigger')
        self.get_logger().info('Safety Trigger Node has been started!')
        self.subscription = self.create_subscription(
            Float64,
            'distance',
            self.distance_callback,
            10)
        
        self.publishers_ = self.create_publisher(String, 'stop', 10)
        
    def distance_callback(self, msg):
        distance = msg.data
        if distance < 2.0:
            self.get_logger().warn(f'Obstacle detected at {distance:.2f} cm! Stopping the robot.')
            stop_msg = String()
            stop_msg.data = "True"
            self.publishers_.publish(stop_msg)
        else:
            self.get_logger().info(f'No obstacle detected. Current distance: {distance:.2f} cm')
            stop_msg = String()
            stop_msg.data = "False"
            self.publishers_.publish(stop_msg)

    

def main(args=None):
    rclpy.init(args=args)
    node = SafetyTrigger()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()