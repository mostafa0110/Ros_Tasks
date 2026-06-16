import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    # 1. Locate the xacro file inside share
    pkg_share_dir = get_package_share_directory('my_robot_description')
    xacro_file = os.path.join(pkg_share_dir, 'urdf', 'robot.urdf.xacro')

    # 2. Auto-detect ROS distro to select the correct Gazebo plugin.
    #    Humble uses Gazebo Classic (use_gz_sim=false)
    #    Jazzy and newer use Gazebo Sim / Ignition (use_gz_sim=true)
    ros_distro = os.environ.get('ROS_DISTRO', 'jazzy')
    use_gz_sim = 'false' if ros_distro == 'humble' else 'true'

    # 3. Parse the xacro file, passing the distro flag
    robot_description_raw = xacro.process_file(
        xacro_file,
        mappings={'use_gz_sim': use_gz_sim}
    ).toxml()


    # 4. Define the robot_state_publisher node
    #    Subscribes to /joint_states and publishes the full TF tree
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_raw}]
    )

    # 5. Joint state publisher GUI — only for offline URDF verification in RViz.
    #    When running Gazebo, joint_state_broadcaster replaces this node.
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_gui_node
    ])
