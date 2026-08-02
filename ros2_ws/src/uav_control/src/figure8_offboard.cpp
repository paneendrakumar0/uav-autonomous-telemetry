#include <px4_msgs/msg/offboard_control_mode.hpp>
#include <px4_msgs/msg/trajectory_setpoint.hpp>
#include <px4_msgs/msg/vehicle_command.hpp>
#include <rclcpp/rclcpp.hpp>

#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>

using namespace std::chrono_literals;

class Figure8Offboard : public rclcpp::Node
{
public:
	Figure8Offboard() : Node("figure8_offboard")
	{
		amplitude_ = declare_parameter<double>("amplitude", 5.0);
		omega_ = declare_parameter<double>("omega", 0.5);
		altitude_ned_ = declare_parameter<double>("altitude_ned", -5.0);
		yaw_ = declare_parameter<double>("yaw", 0.0);
		arm_after_setpoints_ = declare_parameter<int>("arm_after_setpoints", 50);

		auto qos = rclcpp::QoS(rclcpp::KeepLast(1)).best_effort();
		offboard_control_mode_pub_ =
			create_publisher<px4_msgs::msg::OffboardControlMode>("/fmu/in/offboard_control_mode", qos);
		trajectory_setpoint_pub_ =
			create_publisher<px4_msgs::msg::TrajectorySetpoint>("/fmu/in/trajectory_setpoint", qos);
		vehicle_command_pub_ =
			create_publisher<px4_msgs::msg::VehicleCommand>("/fmu/in/vehicle_command", qos);

		start_time_ = now();
		timer_ = create_wall_timer(20ms, std::bind(&Figure8Offboard::timer_callback, this));

		RCLCPP_INFO(
			get_logger(),
			"Figure-8 offboard started: amplitude=%.2f m, omega=%.2f rad/s, altitude=%.2f m NED",
			amplitude_, omega_, altitude_ned_);
	}

private:
	rclcpp::TimerBase::SharedPtr timer_;
	rclcpp::Publisher<px4_msgs::msg::OffboardControlMode>::SharedPtr offboard_control_mode_pub_;
	rclcpp::Publisher<px4_msgs::msg::TrajectorySetpoint>::SharedPtr trajectory_setpoint_pub_;
	rclcpp::Publisher<px4_msgs::msg::VehicleCommand>::SharedPtr vehicle_command_pub_;

	rclcpp::Time start_time_;
	double amplitude_{5.0};
	double omega_{0.5};
	double altitude_ned_{-5.0};
	double yaw_{0.0};
	int arm_after_setpoints_{50};
	int setpoint_counter_{0};
	bool command_sent_{false};

	uint64_t timestamp_us() const
	{
		return now().nanoseconds() / 1000;
	}

	void publish_vehicle_command(uint16_t command, float param1 = 0.0F, float param2 = 0.0F)
	{
		px4_msgs::msg::VehicleCommand msg{};
		msg.param1 = param1;
		msg.param2 = param2;
		msg.command = command;
		msg.target_system = 1;
		msg.target_component = 1;
		msg.source_system = 1;
		msg.source_component = 1;
		msg.from_external = true;
		msg.timestamp = timestamp_us();
		vehicle_command_pub_->publish(msg);
	}

	void publish_offboard_control_mode()
	{
		px4_msgs::msg::OffboardControlMode msg{};
		msg.position = true;
		msg.velocity = true;
		msg.acceleration = false;
		msg.attitude = false;
		msg.body_rate = false;
		msg.timestamp = timestamp_us();
		offboard_control_mode_pub_->publish(msg);
	}

	void publish_trajectory_setpoint()
	{
		const double t = (now() - start_time_).seconds();
		const double phase = omega_ * t;
		const double sin_phase = std::sin(phase);
		const double cos_phase = std::cos(phase);

		const float x = static_cast<float>(amplitude_ * sin_phase);
		const float y = static_cast<float>(amplitude_ * sin_phase * cos_phase);
		const float vx = static_cast<float>(amplitude_ * omega_ * cos_phase);
		const float vy = static_cast<float>(amplitude_ * omega_ * (cos_phase * cos_phase - sin_phase * sin_phase));

		px4_msgs::msg::TrajectorySetpoint msg{};
		msg.position = {x, y, static_cast<float>(altitude_ned_)};
		msg.velocity = {vx, vy, 0.0F};
		msg.yaw = static_cast<float>(yaw_);
		msg.timestamp = timestamp_us();
		trajectory_setpoint_pub_->publish(msg);
	}

	void timer_callback()
	{
		publish_offboard_control_mode();
		publish_trajectory_setpoint();

		if (!command_sent_ && setpoint_counter_ >= arm_after_setpoints_) {
			publish_vehicle_command(px4_msgs::msg::VehicleCommand::VEHICLE_CMD_DO_SET_MODE, 1.0F, 6.0F);
			publish_vehicle_command(px4_msgs::msg::VehicleCommand::VEHICLE_CMD_COMPONENT_ARM_DISARM, 1.0F);
			command_sent_ = true;
			RCLCPP_INFO(get_logger(), "Sent offboard mode and arm commands");
		}

		++setpoint_counter_;
	}
};

int main(int argc, char * argv[])
{
	rclcpp::init(argc, argv);
	rclcpp::spin(std::make_shared<Figure8Offboard>());
	rclcpp::shutdown();
	return 0;
}
