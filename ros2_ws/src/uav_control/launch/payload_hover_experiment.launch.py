from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    metrics_path = LaunchConfiguration("metrics_path")
    payload_metrics_path = LaunchConfiguration("payload_metrics_path")
    altitude_ned = LaunchConfiguration("altitude_ned")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "metrics_path",
                default_value="payload_hover_tracking_metrics.csv",
                description="CSV path for hover tracking metrics.",
            ),
            DeclareLaunchArgument(
                "payload_metrics_path",
                default_value="payload_hover_swing_metrics.csv",
                description="CSV path for slung-payload swing metrics.",
            ),
            DeclareLaunchArgument(
                "altitude_ned",
                default_value="-5.0",
                description="Commanded hover altitude in PX4 NED coordinates.",
            ),
            Node(
                package="uav_control",
                executable="figure8_metrics_logger",
                name="hover_metrics_logger",
                output="screen",
                parameters=[{"output_path": metrics_path}],
            ),
            Node(
                package="uav_control",
                executable="payload_swing_logger",
                name="payload_swing_logger",
                output="screen",
                parameters=[{"output_path": payload_metrics_path}],
            ),
            Node(
                package="uav_control",
                executable="hover_offboard",
                name="hover_offboard",
                output="screen",
                parameters=[
                    {
                        "x": 0.0,
                        "y": 0.0,
                        "altitude_ned": altitude_ned,
                        "yaw": 0.0,
                        "arm_after_setpoints": 50,
                    }
                ],
            ),
        ]
    )
