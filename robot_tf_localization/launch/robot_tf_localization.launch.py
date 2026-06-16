from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    pkg_share = get_package_share_directory('robot_tf_localization')
    ekf_config = os.path.join(pkg_share, 'config', 'ekf.yaml')
    rviz_config = os.path.join(pkg_share, 'config', 'robot_tf.rviz')

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    return LaunchDescription([

        # ── Launch arguments (must come before nodes) ───────────────────
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation time'
        ),

        # ── Static transforms ───────────────────────────────────────────

        # base_footprint → base_link  (5 cm up)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='tf_base_footprint_to_base_link',
            arguments=[
                '--x', '0.0', '--y', '0.0', '--z', '0.05',
                '--roll', '0.0', '--pitch', '0.0', '--yaw', '0.0',
                '--frame-id', 'base_footprint',
                '--child-frame-id', 'base_link'
            ]
        ),

        # base_link → imu_link  (5 cm from front = x=0.5, 15 cm above ground → z=0.1)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='tf_base_link_to_imu_link',
            arguments=[
                '--x', '0.5', '--y', '-0.1', '--z', '0.1',
                '--roll', '0.0', '--pitch', '0.0', '--yaw', '0.0',
                '--frame-id', 'base_link',
                '--child-frame-id', 'imu_link'
            ]
        ),

        # base_link → gps_link  (center X = 0.3, 30 cm above ground → z=0.25)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='tf_base_link_to_gps_link',
            arguments=[
                '--x', '0.2', '--y', '0.0', '--z', '0.25',
                '--roll', '0.0', '--pitch', '0.0', '--yaw', '0.0',
                '--frame-id', 'base_link',
                '--child-frame-id', 'gps_link'
            ]
        ),

        # base_link → ultrasonic1_link  Front-Left  +45°
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='tf_base_link_to_ultrasonic1',
            arguments=[
                '--x', '0.5', '--y', '0.15', '--z', '0.1',
                '--roll', '0.0', '--pitch', '0.0', '--yaw', '0.785398163',
                '--frame-id', 'base_link',
                '--child-frame-id', 'ultrasonic1_link'
            ]
        ),

        # base_link → ultrasonic2_link  Front-Center  0°
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='tf_base_link_to_ultrasonic2',
            arguments=[
                '--x', '0.5', '--y', '0.0', '--z', '0.1',
                '--roll', '0.0', '--pitch', '0.0', '--yaw', '0.0',
                '--frame-id', 'base_link',
                '--child-frame-id', 'ultrasonic2_link'
            ]
        ),

        # base_link → ultrasonic3_link  Front-Right  -45°
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='tf_base_link_to_ultrasonic3',
            arguments=[
                '--x', '0.5', '--y', '-0.15', '--z', '0.1',
                '--roll', '0.0', '--pitch', '0.0', '--yaw', '-0.785398163',
                '--frame-id', 'base_link',
                '--child-frame-id', 'ultrasonic3_link'
            ]
        ),

        # base_link → ultrasonic4_link  Rear-Left  +135°
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='tf_base_link_to_ultrasonic4',
            arguments=[
                '--x', '-0.1', '--y', '0.15', '--z', '0.1',
                '--roll', '0.0', '--pitch', '0.0', '--yaw', '2.35619449',
                '--frame-id', 'base_link',
                '--child-frame-id', 'ultrasonic4_link'
            ]
        ),

        # base_link → ultrasonic5_link  Rear-Center  180°
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='tf_base_link_to_ultrasonic5',
            arguments=[
                '--x', '-0.1', '--y', '0.0', '--z', '0.1',
                '--roll', '0.0', '--pitch', '0.0', '--yaw', '3.141592654',
                '--frame-id', 'base_link',
                '--child-frame-id', 'ultrasonic5_link'
            ]
        ),

        # base_link → ultrasonic6_link  Rear-Right  -135°
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='tf_base_link_to_ultrasonic6',
            arguments=[
                '--x', '-0.1', '--y', '-0.15', '--z', '0.1',
                '--roll', '0.0', '--pitch', '0.0', '--yaw', '-2.35619449',
                '--frame-id', 'base_link',
                '--child-frame-id', 'ultrasonic6_link'
            ]
        ),

        # ── robot_localization EKF (local: odom → base_footprint) ───────
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node_odom',
            output='screen',
            parameters=[
                ekf_config,
                {'use_sim_time': use_sim_time}
            ],
            remappings=[
                ('/odometry/wheel', '/odometry/wheel'),   # bag remap handled at playback
                ('/imu/data',       '/imu/data'),
                ('odometry/filtered', '/odometry/local'),
            ]
        ),

        # ── orientation_analysis node ────────────────────────────────────
        Node(
            package='robot_tf_localization',
            executable='orientation_analysis.py',
            name='orientation_analysis',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}]
        ),

        # ── RViz ────────────────────────────────────────────────────────
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_config],
            parameters=[{'use_sim_time': use_sim_time}]
        ),
    ])