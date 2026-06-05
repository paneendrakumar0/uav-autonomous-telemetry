#include <px4_msgs/msg/offboard_control_mode.hpp>
#include <px4_msgs/msg/trajectory_setpoint.hpp>
#include <px4_msgs/msg/vehicle_command.hpp>
#include <rclcpp/rclcpp.hpp>

#include <array>
#include <chrono>
#include <cstdint>

using namespace std::chrono_literals;

class HoverOffboard : public rclcpp::Node
{
public:
	HoverOffboard() : Node("hover_offboard")
	{
		x_ = declare_parameter<double>("x", 0.0);
		y_ = declare_parameter<double>("y", 0.0);
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

		timer_ = create_wall_timer(20ms, std::bind(&HoverOffboard::timer_callback, this));
		RCLCPP_INFO(
			get_logger(),
			"Hover offboard started: target=(%.2f, %.2f, %.2f NED), yaw=%.2f",
			x_, y_, altitude_ned_, yaw_);
	}

private:
	rclcpp::TimerBase::SharedPtr timer_;
	rclcpp::Publisher<px4_msgs::msg::OffboardControlMode>::SharedPtr offboard_control_mode_pub_;
	rclcpp::Publisher<px4_msgs::msg::TrajectorySetpoint>::SharedPtr trajectory_setpoint_pub_;
	rclcpp::Publisher<px4_msgs::msg::VehicleCommand>::SharedPtr vehicle_command_pub_;

	double x_{0.0};
	double y_{0.0};
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
		msg.velocity = false;
		msg.acceleration = false;
		msg.attitude = false;
		msg.body_rate = false;
		msg.timestamp = timestamp_us();
		offboard_control_mode_pub_->publish(msg);
	}

	void publish_trajectory_setpoint()
	{
		px4_msgs::msg::TrajectorySetpoint msg{};
		msg.position = {
			static_cast<float>(x_),
			static_cast<float>(y_),
			static_cast<float>(altitude_ned_),
		};
		msg.velocity = {0.0F, 0.0F, 0.0F};
		msg.yaw = static_cast<float>(yaw_);
		msg.timestamp = timestamp_us();
		trajectory_setpoint_pub_->publish(msg);
	}

	void timer_callback()
	{
		publish_offboard_control_mode();
		publish_trajectory_setpoint();

		if (!command_sent_ && setpoint_counter_ >= arm_after_setpoints_) {
			publish_vehicle_command(px4_msgs::msg::VehicleCommand::VEHICLE_CMD_COMPONENT_ARM_DISARM, 1.0F);
			publish_vehicle_command(px4_msgs::msg::VehicleCommand::VEHICLE_CMD_DO_SET_MODE, 1.0F, 6.0F);
			command_sent_ = true;
			RCLCPP_INFO(get_logger(), "Sent arm and offboard mode commands");
		}

		++setpoint_counter_;
	}
};

int main(int argc, char * argv[])
{
	rclcpp::init(argc, argv);
	rclcpp::spin(std::make_shared<HoverOffboard>());
	rclcpp::shutdown();
	return 0;
}
