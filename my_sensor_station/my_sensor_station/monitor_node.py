#!/usr/bin/env python3
"""
monitor_node - Fuses LiDAR + ultrasonic data and publishes alerts.

Subscribes: /scan, /ultrasonic, /pot_threshold
Publishes:  /min_distance, /alert
Parameter:  alert_threshold (default 0.8 m)
"""

import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Range
from std_msgs.msg import Float32, Bool


class MonitorNode(Node):
    def __init__(self):
        super().__init__('monitor_node')

        # Parameter
        self.declare_parameter('alert_threshold', 0.8)
        self.alert_threshold = self.get_parameter('alert_threshold').value

        # Sensor data storage
        self.lidar_min = float('inf')
        self.ultrasonic_dist = float('inf')

        # Subscribers
        self.create_subscription(LaserScan, '/scan', self.scan_cb, 10)
        self.create_subscription(Range, '/ultrasonic', self.ultrasonic_cb, 10)
        self.create_subscription(Float32, '/pot_threshold', self.pot_cb, 10)

        # Publishers
        self.min_dist_pub = self.create_publisher(Float32, '/min_distance', 10)
        self.alert_pub = self.create_publisher(Bool, '/alert', 10)

        # Timer to publish at 10 Hz
        self.create_timer(0.1, self.timer_cb)

        self.get_logger().info(f'MonitorNode started (threshold={self.alert_threshold}m)')

    def scan_cb(self, msg):
        """Get min distance from LaserScan + print basic stats."""
        # Filter out invalid readings
        valid = [r for r in msg.ranges
                 if msg.range_min <= r <= msg.range_max and math.isfinite(r)]

        if valid:
            self.lidar_min = min(valid)
            avg = sum(valid) / len(valid)
            self.get_logger().info(
                f'LiDAR: min={self.lidar_min:.2f}m, max={max(valid):.2f}m, '
                f'avg={avg:.2f}m, valid={len(valid)}/{len(msg.ranges)}'
            )

    def ultrasonic_cb(self, msg):
        """Store latest ultrasonic reading."""
        self.ultrasonic_dist = msg.range

    def pot_cb(self, msg):
        """Update threshold from potentiometer."""
        self.alert_threshold = msg.data
        self.get_logger().info(f'Threshold updated from pot: {msg.data:.2f}m')

    def timer_cb(self):
        """Fuse sensors, publish min_distance and alert."""
        # Also check if parameter was changed via 'ros2 param set'
        self.alert_threshold = self.get_parameter('alert_threshold').value

        # Fused minimum
        min_dist = min(self.lidar_min, self.ultrasonic_dist)

        # Publish /min_distance
        dist_msg = Float32()
        dist_msg.data = min_dist if math.isfinite(min_dist) else -1.0
        self.min_dist_pub.publish(dist_msg)

        # Publish /alert
        alert_msg = Bool()
        alert_msg.data = math.isfinite(min_dist) and min_dist < self.alert_threshold
        self.alert_pub.publish(alert_msg)

        if alert_msg.data:
            self.get_logger().warn(
                f'ALERT! min_dist={min_dist:.2f}m < threshold={self.alert_threshold:.2f}m'
            )


def main(args=None):
    rclpy.init(args=args)
    node = MonitorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
