from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    metrics_path = LaunchConfiguration("metrics_path")
    amplitude = LaunchConfiguration("amplitude")
    omega = LaunchConfiguration("omega")
    altitude_ned = LaunchConfiguration("altitude_ned")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "metrics_path",
                default_value="figure8_tracking_metrics.csv",
                description="CSV path for actual/reference trajectory tracking metrics.",
            ),
            DeclareLaunchArgument(
                "amplitude",
                default_value="5.0",
                description="Figure-8 x-axis amplitude in metres.",
            ),
            DeclareLaunchArgument(
                "omega",
                default_value="0.25",
                description="Figure-8 angular rate in rad/s.",
            ),
            DeclareLaunchArgument(
                "altitude_ned",
                default_value="-5.0",
                description="Commanded altitude in PX4 NED coordinates.",
            ),
            Node(
                package="uav_control",
                executable="figure8_metrics_logger",
                name="figure8_metrics_logger",
                output="screen",
                parameters=[{"output_path": metrics_path}],
            ),
            Node(
                package="uav_control",
                executable="figure8_offboard",
                name="figure8_offboard",
                output="screen",
                parameters=[
                    {
                        "amplitude": amplitude,
                        "omega": omega,
                        "altitude_ned": altitude_ned,
                        "yaw": 0.0,
                        "arm_after_setpoints": 50,
                    }
                ],
            ),
        ]
    )
