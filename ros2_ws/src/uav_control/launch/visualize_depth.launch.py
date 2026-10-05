import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    rviz_config_dir = os.path.join(
        get_package_share_directory('uav_control'),
        'rviz',
        'depth_mapping.rviz')

    return LaunchDescription([
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen'
        ),
        # A static transform publisher from 'map' or 'odom' to 'camera_link_optical'
        # Since PX4 offboard handles localization, we just link odom to the camera frame
        # for quick visualization before the mapping node is fully developed.
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='camera_tf_broadcaster',
            arguments=['0.1', '0', '0', '-1.57', '0', '-1.57', 'base_link', 'camera_link_optical'],
            output='screen'
        )
    ])
