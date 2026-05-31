from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='task1',
            executable='pub_node',
            name='minimal_publisher',
            output='screen',
        ),
        Node(
            package='task1',
            executable='sub_node',
            name='minimal_subscriber',
            output='screen',
        ),
    ])