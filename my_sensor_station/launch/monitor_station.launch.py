"""
Launch file for the Sensor Monitoring Station.

Starts: rplidar_node, arduino_bridge, monitor_node

Usage:
  ros2 launch my_sensor_station monitor_station.launch.py
  ros2 launch my_sensor_station monitor_station.launch.py alert_threshold:=1.2
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    # Launch argument to override threshold from terminal
    threshold_arg = DeclareLaunchArgument(
        'alert_threshold',
        default_value='0.8',
        description='Alert threshold in meters'
    )

    # 1. RPLIDAR node (publishes /scan)
    rplidar = Node(
        package='rplidar_ros',
        executable='rplidar_node',
        name='rplidar_node',
        output='screen',
        parameters=[{
            'serial_port': '/dev/ttyUSB0',
            'frame_id': 'laser',
        }],
    )

    # 2. Arduino bridge (publishes /ultrasonic and /pot_threshold)
    arduino = Node(
        package='my_sensor_station',
        executable='arduino_bridge',
        name='arduino_bridge',
        output='screen',
    )

    # 3. Monitor node (subscribes to everything, publishes alerts)
    monitor = Node(
        package='my_sensor_station',
        executable='monitor_node',
        name='monitor_node',
        output='screen',
        parameters=[{
            'alert_threshold': LaunchConfiguration('alert_threshold'),
        }],
    )

    return LaunchDescription([
        threshold_arg,
        rplidar,
        arduino,
        monitor,
    ])
