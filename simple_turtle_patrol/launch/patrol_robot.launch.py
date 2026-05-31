import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    # Path to the parameter file
    params_file = os.path.join(
        get_package_share_directory('simple_turtle_patrol'),
        'params',
        'patrol_params.yaml'
    )

    return LaunchDescription([
        # 1. Turtlesim node
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim_node',
            output='screen',
        ),

        # 2. Status publisher node
        Node(
            package='simple_turtle_patrol',
            executable='status_publisher',
            name='status_publisher',
            output='screen',
            parameters=[params_file],
        ),

        # 3. Patrol controller node
        Node(
            package='simple_turtle_patrol',
            executable='patrol_controller',
            name='patrol_controller',
            output='screen',
            parameters=[params_file],
        ),
    ])
