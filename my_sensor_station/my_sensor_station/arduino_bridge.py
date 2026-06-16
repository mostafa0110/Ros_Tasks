#!/usr/bin/env python3
"""
arduino_bridge - Reads serial data from Arduino and publishes to ROS 2.

Arduino sends lines like: "distance_cm,pot_value"
Example: "25.3,512"

Publishes:
  /ultrasonic     (sensor_msgs/Range)   - distance in meters
  /pot_threshold  (std_msgs/Float32)    - threshold in meters (mapped from 0-1023)
"""

import serial
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from std_msgs.msg import Float32


class ArduinoBridge(Node):
    def __init__(self):
        super().__init__('arduino_bridge')

        # Serial port setup (Arduino)
        self.serial_port = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.get_logger().info('Connected to Arduino on /dev/ttyACM0')

        # Publishers
        self.ultra_pub = self.create_publisher(Range, '/ultrasonic', 10)
        self.pot_pub = self.create_publisher(Float32, '/pot_threshold', 10)

        # Timer to read serial at 20 Hz
        self.create_timer(0.05, self.read_serial)

    def read_serial(self):
        """Read one line from Arduino and publish both topics."""
        if self.serial_port.in_waiting > 0:
            try:
                line = self.serial_port.readline().decode('utf-8').strip()
                parts = line.split(',')

                if len(parts) == 2:
                    distance_cm = float(parts[0])
                    pot_value = float(parts[1])

                    # Publish ultrasonic range (convert cm to meters)
                    range_msg = Range()
                    range_msg.header.stamp = self.get_clock().now().to_msg()
                    range_msg.header.frame_id = 'ultrasonic'
                    range_msg.radiation_type = Range.ULTRASOUND
                    range_msg.field_of_view = 0.26   # ~15 degrees
                    range_msg.min_range = 0.02       # 2 cm
                    range_msg.max_range = 4.0        # 400 cm
                    range_msg.range = distance_cm / 100.0  # cm -> m
                    self.ultra_pub.publish(range_msg)

                    # Publish pot threshold (map 0-1023 to 0.2-3.0 meters)
                    threshold = 0.2 + (pot_value / 1023.0) * 2.8
                    pot_msg = Float32()
                    pot_msg.data = threshold
                    self.pot_pub.publish(pot_msg)

            except Exception as e:
                self.get_logger().warn(f'Serial read error: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = ArduinoBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
