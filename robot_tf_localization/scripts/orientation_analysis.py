#!/usr/bin/env python3
"""
orientation_analysis.py
Lab 3 — compares yaw from IMU (/imu/data) vs EKF output (/odometry/local).
Uses qos_profile_sensor_data to match the Best-Effort bag QoS.
"""

import math
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry


def quat_to_yaw(q):
    """Convert a quaternion to yaw (rotation about Z axis) in degrees."""
    siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
    return math.degrees(math.atan2(siny_cosp, cosy_cosp))


class OrientationAnalysis(Node):

    def __init__(self):
        super().__init__('orientation_analysis')

        self._imu_yaw = None
        self._ekf_yaw = None

        # Subscribe with sensor_data QoS (Best Effort) to match bag recording
        self.create_subscription(
            Imu,
            '/imu/data',
            self._imu_cb,
            qos_profile_sensor_data
        )

        self.create_subscription(
            Odometry,
            '/odometry/local',
            self._odom_cb,
            qos_profile_sensor_data
        )

        # Log comparison every second
        self.create_timer(1.0, self._timer_cb)

        self.get_logger().info('OrientationAnalysis node started.')
        self.get_logger().info('  Subscribing to /imu/data        (Best Effort QoS)')
        self.get_logger().info('  Subscribing to /odometry/local  (Best Effort QoS)')

    def _imu_cb(self, msg: Imu):
        self._imu_yaw = quat_to_yaw(msg.orientation)

    def _odom_cb(self, msg: Odometry):
        self._ekf_yaw = quat_to_yaw(msg.pose.pose.orientation)

    def _timer_cb(self):
        if self._imu_yaw is None and self._ekf_yaw is None:
            self.get_logger().warn('Waiting for data on /imu/data and /odometry/local ...')
            return

        imu_str = f'{self._imu_yaw:+.2f}°' if self._imu_yaw is not None else 'N/A'
        ekf_str = f'{self._ekf_yaw:+.2f}°' if self._ekf_yaw is not None else 'N/A'

        diff_str = 'N/A'
        if self._imu_yaw is not None and self._ekf_yaw is not None:
            diff = self._ekf_yaw - self._imu_yaw
            # Normalize to [-180, 180]
            diff = (diff + 180.0) % 360.0 - 180.0
            diff_str = f'{diff:+.2f}°'

        self.get_logger().info(
            f'\n--- Orientation Comparison ---\n'
            f'  IMU yaw          : {imu_str}\n'
            f'  EKF (local) yaw  : {ekf_str}\n'
            f'  Difference       : {diff_str}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = OrientationAnalysis()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
