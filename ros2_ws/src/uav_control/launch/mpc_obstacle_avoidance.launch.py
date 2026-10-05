import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    uav_control_dir = get_package_share_directory('uav_control')

    return LaunchDescription([
        # 1. Start the 3D Volumetric Mapping Node
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(uav_control_dir, 'launch', 'octomap.launch.py')
            )
        ),
        
        # 2. Start the Payload-Aware MPC Node
        Node(
            package='uav_control',
            executable='mpc_trajectory_planner',
            name='mpc_trajectory_planner',
            output='screen'
        ),

        # 3. Start the Low-Level Offboard Controller (executes MPC setpoints)
        Node(
            package='uav_control',
            executable='offboard_control',
            name='offboard_control',
            output='screen'
        ),
        
        # 4. Broadcast Static Transforms for Depth Camera Vision
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='camera_tf_broadcaster',
            arguments=['0.1', '0', '0', '-1.57', '0', '-1.57', 'base_link', 'camera_link_optical'],
            output='screen'
        )
    ])
