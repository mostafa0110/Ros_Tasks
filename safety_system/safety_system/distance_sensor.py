import rclpy
from rclpy.node import Node
import random
from std_msgs.msg import Float64

class DistanceSensor(Node):
    def __init__(self):
        super().__init__('distance_sensor')
        self.get_logger().info('Distance Sensor Node has been started!')
        self.publisher_ = self.create_publisher(Float64, 'distance', 10)
        timer_period = 1  
        self.timer = self.create_timer(timer_period, self.timer_callback)


    def read_distance(self):
        # Simulate reading distance from a sensor
        distance = random.uniform(0.03, 5)
        return distance
    
    def timer_callback(self):
        msg = Float64()
        msg.data = self.read_distance()
        self.publisher_.publish(msg)
        self.get_logger().info('Published distance: "%.2f cm"' % msg.data)


    

def main(args=None):
    rclpy.init(args=args)
    node = DistanceSensor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()