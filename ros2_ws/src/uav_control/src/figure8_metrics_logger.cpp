#include <px4_msgs/msg/trajectory_setpoint.hpp>
#include <px4_msgs/msg/vehicle_local_position.hpp>
#include <rclcpp/rclcpp.hpp>

#include <array>
#include <chrono>
#include <cmath>
#include <cstddef>
#include <fstream>
#include <limits>
#include <string>

class Figure8MetricsLogger : public rclcpp::Node
{
public:
	Figure8MetricsLogger() : Node("figure8_metrics_logger")
	{
		output_path_ = declare_parameter<std::string>("output_path", "figure8_tracking_metrics.csv");
		csv_.open(output_path_, std::ios::out | std::ios::trunc);
		csv_ << "timestamp_us,t_s,actual_x,actual_y,actual_z,reference_x,reference_y,reference_z,"
			"error_x,error_y,error_z,error_norm,actual_vx,actual_vy,actual_vz,reference_vx,reference_vy,reference_vz\n";

		auto qos = rclcpp::QoS(rclcpp::KeepLast(20)).best_effort();
		local_position_sub_ = create_subscription<px4_msgs::msg::VehicleLocalPosition>(
			"/fmu/out/vehicle_local_position_v1", qos,
			std::bind(&Figure8MetricsLogger::local_position_callback, this, std::placeholders::_1));

		setpoint_sub_ = create_subscription<px4_msgs::msg::TrajectorySetpoint>(
			"/fmu/in/trajectory_setpoint", qos,
			std::bind(&Figure8MetricsLogger::setpoint_callback, this, std::placeholders::_1));

		RCLCPP_INFO(get_logger(), "Figure-8 metrics logger writing to %s", output_path_.c_str());
	}

	~Figure8MetricsLogger() override
	{
		if (csv_.is_open()) {
			csv_.close();
		}

		if (sample_count_ > 0) {
			const double mean_error = error_sum_ / static_cast<double>(sample_count_);
			const double rms_error = std::sqrt(error_sq_sum_ / static_cast<double>(sample_count_));
			RCLCPP_INFO(
				get_logger(),
				"samples=%zu mean_error=%.3f m rms_error=%.3f m max_error=%.3f m",
				sample_count_, mean_error, rms_error, max_error_);
		}
	}

private:
	rclcpp::Subscription<px4_msgs::msg::VehicleLocalPosition>::SharedPtr local_position_sub_;
	rclcpp::Subscription<px4_msgs::msg::TrajectorySetpoint>::SharedPtr setpoint_sub_;

	std::ofstream csv_;
	std::string output_path_;
	std::array<float, 3> reference_position_{0.0F, 0.0F, -5.0F};
	std::array<float, 3> reference_velocity_{0.0F, 0.0F, 0.0F};
	bool have_reference_{false};
	uint64_t first_timestamp_us_{0};
	std::size_t sample_count_{0};
	double error_sum_{0.0};
	double error_sq_sum_{0.0};
	double max_error_{0.0};

	void setpoint_callback(const px4_msgs::msg::TrajectorySetpoint::SharedPtr msg)
	{
		reference_position_ = msg->position;
		reference_velocity_ = msg->velocity;
		have_reference_ = true;
	}

	void local_position_callback(const px4_msgs::msg::VehicleLocalPosition::SharedPtr msg)
	{
		if (!have_reference_ || !msg->xy_valid || !msg->z_valid) {
			return;
		}

		if (first_timestamp_us_ == 0) {
			first_timestamp_us_ = msg->timestamp;
		}

		const double t_s = static_cast<double>(msg->timestamp - first_timestamp_us_) * 1e-6;
		const double error_x = static_cast<double>(msg->x - reference_position_[0]);
		const double error_y = static_cast<double>(msg->y - reference_position_[1]);
		const double error_z = static_cast<double>(msg->z - reference_position_[2]);
		const double error_norm = std::sqrt(error_x * error_x + error_y * error_y + error_z * error_z);

		error_sum_ += error_norm;
		error_sq_sum_ += error_norm * error_norm;
		max_error_ = std::max(max_error_, error_norm);
		++sample_count_;

		csv_ << msg->timestamp << ','
			<< t_s << ','
			<< msg->x << ','
			<< msg->y << ','
			<< msg->z << ','
			<< reference_position_[0] << ','
			<< reference_position_[1] << ','
			<< reference_position_[2] << ','
			<< error_x << ','
			<< error_y << ','
			<< error_z << ','
			<< error_norm << ','
			<< msg->vx << ','
			<< msg->vy << ','
			<< msg->vz << ','
			<< reference_velocity_[0] << ','
			<< reference_velocity_[1] << ','
			<< reference_velocity_[2] << '\n';
	}
};

int main(int argc, char * argv[])
{
	rclcpp::init(argc, argv);
	rclcpp::spin(std::make_shared<Figure8MetricsLogger>());
	rclcpp::shutdown();
	return 0;
}
