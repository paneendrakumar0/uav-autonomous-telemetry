import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='octomap_server',
            executable='octomap_server_node',
            name='octomap_server',
            output='screen',
            parameters=[
                {'resolution': 0.15},
                {'frame_id': 'odom'},
                {'base_frame_id': 'base_link'},
                {'sensor_model.max_range': 10.0},
                {'sensor_model.hit': 0.7},
                {'sensor_model.miss': 0.4},
                {'latch': False}
            ],
            remappings=[
                ('cloud_in', '/camera/depth/points')
            ]
        )
    ])
