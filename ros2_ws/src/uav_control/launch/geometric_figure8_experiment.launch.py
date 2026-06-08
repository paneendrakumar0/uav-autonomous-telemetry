from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    metrics_path = LaunchConfiguration("metrics_path")
    payload_metrics_path = LaunchConfiguration("payload_metrics_path")
    amplitude = LaunchConfiguration("amplitude")
    omega = LaunchConfiguration("omega")
    altitude_ned = LaunchConfiguration("altitude_ned")
    hover_thrust = LaunchConfiguration("hover_thrust")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "metrics_path",
                default_value="geometric_figure8_tracking_metrics.csv",
                description="CSV path for actual/reference trajectory tracking metrics.",
            ),
            DeclareLaunchArgument(
                "payload_metrics_path",
                default_value="geometric_payload_swing_metrics.csv",
                description="CSV path for slung-payload swing metrics.",
            ),
            DeclareLaunchArgument(
                "amplitude",
                default_value="5.0",
                description="Figure-8 x-axis amplitude in metres.",
            ),
            DeclareLaunchArgument(
                "omega",
                default_value="0.20",
                description="Figure-8 angular rate in rad/s. Start slightly slower for attitude-mode commissioning.",
            ),
            DeclareLaunchArgument(
                "altitude_ned",
                default_value="-5.0",
                description="Commanded altitude in PX4 NED coordinates.",
            ),
            DeclareLaunchArgument(
                "hover_thrust",
                default_value="0.62",
                description="Normalized hover-thrust estimate used to scale attitude-mode thrust.",
            ),
            Node(
                package="uav_control",
                executable="figure8_metrics_logger",
                name="geometric_figure8_metrics_logger",
                output="screen",
                parameters=[{"output_path": metrics_path}],
            ),
            Node(
                package="uav_control",
                executable="payload_swing_logger",
                name="geometric_payload_swing_logger",
                output="screen",
                parameters=[{"output_path": payload_metrics_path}],
            ),
            Node(
                package="uav_control",
                executable="geometric_figure8_attitude",
                name="geometric_figure8_attitude",
                output="screen",
                parameters=[
                    {
                        "amplitude": amplitude,
                        "omega": omega,
                        "altitude_ned": altitude_ned,
                        "hover_thrust": hover_thrust,
                        "kp_xy": 1.4,
                        "kp_z": 2.2,
                        "kd_xy": 1.1,
                        "kd_z": 1.4,
                        "takeoff_ramp_s": 8.0,
                        "arm_after_setpoints": 50,
                    }
                ],
            ),
        ]
    )
