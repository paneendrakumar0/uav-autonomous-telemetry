#include <px4_msgs/msg/offboard_control_mode.hpp>
#include <px4_msgs/msg/trajectory_setpoint.hpp>
#include <px4_msgs/msg/vehicle_attitude_setpoint.hpp>
#include <px4_msgs/msg/vehicle_command.hpp>
#include <px4_msgs/msg/vehicle_status.hpp>
#include <px4_msgs/msg/vehicle_local_position.hpp>
#include <geometry_msgs/msg/vector3_stamped.hpp>
#include <rclcpp/rclcpp.hpp>

#include "uav_control/geometric_control_utils.hpp"

#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <string>

using namespace std::chrono_literals;

namespace
{
constexpr double kGravity = 9.80665;

using Vec3 = uav_control::Vector3;

struct Quat
{
	double w{1.0};
	double x{0.0};
	double y{0.0};
	double z{0.0};
};

Vec3 operator-(const Vec3 & a, const Vec3 & b)
{
	return {a.x - b.x, a.y - b.y, a.z - b.z};
}

Vec3 operator*(double s, const Vec3 & v)
{
	return {s * v.x, s * v.y, s * v.z};
}

double dot(const Vec3 & a, const Vec3 & b)
{
	return a.x * b.x + a.y * b.y + a.z * b.z;
}

Vec3 cross(const Vec3 & a, const Vec3 & b)
{
	return {
		a.y * b.z - a.z * b.y,
		a.z * b.x - a.x * b.z,
		a.x * b.y - a.y * b.x,
	};
}

double norm(const Vec3 & v)
{
	return std::sqrt(dot(v, v));
}

double clamp(double value, double low, double high)
{
	return std::max(low, std::min(value, high));
}

Vec3 normalized(const Vec3 & v, const Vec3 & fallback)
{
	const double n = norm(v);
	if (n < 1e-6) {
		return fallback;
	}
	return (1.0 / n) * v;
}

Quat rotation_matrix_to_quaternion(const Vec3 & c0, const Vec3 & c1, const Vec3 & c2)
{
	const double r00 = c0.x;
	const double r01 = c1.x;
	const double r02 = c2.x;
	const double r10 = c0.y;
	const double r11 = c1.y;
	const double r12 = c2.y;
	const double r20 = c0.z;
	const double r21 = c1.z;
	const double r22 = c2.z;

	Quat q{};
	const double trace = r00 + r11 + r22;
	if (trace > 0.0) {
		const double s = std::sqrt(trace + 1.0) * 2.0;
		q.w = 0.25 * s;
		q.x = (r21 - r12) / s;
		q.y = (r02 - r20) / s;
		q.z = (r10 - r01) / s;
	} else if ((r00 > r11) && (r00 > r22)) {
		const double s = std::sqrt(1.0 + r00 - r11 - r22) * 2.0;
		q.w = (r21 - r12) / s;
		q.x = 0.25 * s;
		q.y = (r01 + r10) / s;
		q.z = (r02 + r20) / s;
	} else if (r11 > r22) {
		const double s = std::sqrt(1.0 + r11 - r00 - r22) * 2.0;
		q.w = (r02 - r20) / s;
		q.x = (r01 + r10) / s;
		q.y = 0.25 * s;
		q.z = (r12 + r21) / s;
	} else {
		const double s = std::sqrt(1.0 + r22 - r00 - r11) * 2.0;
		q.w = (r10 - r01) / s;
		q.x = (r02 + r20) / s;
		q.y = (r12 + r21) / s;
		q.z = 0.25 * s;
	}

	const double q_norm = std::sqrt(q.w * q.w + q.x * q.x + q.y * q.y + q.z * q.z);
	if (q_norm > 1e-6) {
		q.w /= q_norm;
		q.x /= q_norm;
		q.y /= q_norm;
		q.z /= q_norm;
	}
	return q;
}
} // namespace

class GeometricFigure8Attitude : public rclcpp::Node
{
public:
	GeometricFigure8Attitude() : Node("geometric_figure8_attitude")
	{
		amplitude_ = declare_parameter<double>("amplitude", 5.0);
		omega_ = declare_parameter<double>("omega", 0.25);
		altitude_ned_ = declare_parameter<double>("altitude_ned", -5.0);
		kp_xy_ = declare_parameter<double>("kp_xy", 1.4);
		kp_z_ = declare_parameter<double>("kp_z", 2.2);
		kd_xy_ = declare_parameter<double>("kd_xy", 1.1);
		kd_z_ = declare_parameter<double>("kd_z", 1.4);
		ki_xy_ = declare_parameter<double>("ki_xy", 0.0);
		ki_z_ = declare_parameter<double>("ki_z", 0.0);
		integral_limit_xy_ = declare_parameter<double>("integral_limit_xy", 5.0);
		integral_limit_z_ = declare_parameter<double>("integral_limit_z", 2.0);
		integrator_leak_rate_ = declare_parameter<double>("integrator_leak_rate", 0.02);
		max_tilt_deg_ = declare_parameter<double>("max_tilt_deg", 35.0);
		disturbance_observer_gain_ = declare_parameter<double>("disturbance_observer_gain", 0.0);
		disturbance_filter_hz_ = declare_parameter<double>("disturbance_filter_hz", 0.5);
		disturbance_limit_xy_ = declare_parameter<double>("disturbance_limit_xy", 3.0);
		payload_swing_kp_ = declare_parameter<double>("payload_swing_kp", 0.0);
		payload_swing_kd_ = declare_parameter<double>("payload_swing_kd", 0.0);
		payload_correction_limit_xy_ = declare_parameter<double>("payload_correction_limit_xy", 2.0);
		payload_state_timeout_s_ = declare_parameter<double>("payload_state_timeout_s", 0.15);
		hover_thrust_ = declare_parameter<double>("hover_thrust", 0.72);
		min_thrust_ = declare_parameter<double>("min_thrust", 0.15);
		max_thrust_ = declare_parameter<double>("max_thrust", 0.90);
		takeoff_ramp_s_ = declare_parameter<double>("takeoff_ramp_s", 8.0);
		attitude_setpoint_topic_ =
			declare_parameter<std::string>("attitude_setpoint_topic", "/fmu/in/vehicle_attitude_setpoint");
		arm_after_setpoints_ = declare_parameter<int>("arm_after_setpoints", 50);

		auto qos = rclcpp::QoS(rclcpp::KeepLast(10)).best_effort();
		local_position_sub_ = create_subscription<px4_msgs::msg::VehicleLocalPosition>(
			"/fmu/out/vehicle_local_position", qos,
			std::bind(&GeometricFigure8Attitude::local_position_callback, this, std::placeholders::_1));
		payload_direction_sub_ = create_subscription<geometry_msgs::msg::Vector3Stamped>(
			"/uav_control/payload_cable_direction", qos,
			[this](geometry_msgs::msg::Vector3Stamped::SharedPtr msg) {
				if (std::isfinite(msg->vector.x) && std::isfinite(msg->vector.y) && std::isfinite(msg->vector.z)) {
					payload_cable_direction_ = {msg->vector.x, msg->vector.y, msg->vector.z};
					payload_state_time_ns_ = now().nanoseconds();
					have_payload_direction_ = true;
				}
			});
		payload_direction_rate_sub_ = create_subscription<geometry_msgs::msg::Vector3Stamped>(
			"/uav_control/payload_cable_direction_rate", qos,
			[this](geometry_msgs::msg::Vector3Stamped::SharedPtr msg) {
				if (std::isfinite(msg->vector.x) && std::isfinite(msg->vector.y) && std::isfinite(msg->vector.z)) {
					payload_cable_direction_rate_ = {msg->vector.x, msg->vector.y, msg->vector.z};
				}
			});
		offboard_control_mode_pub_ =
			create_publisher<px4_msgs::msg::OffboardControlMode>("/fmu/in/offboard_control_mode", qos);
		attitude_setpoint_pub_ =
			create_publisher<px4_msgs::msg::VehicleAttitudeSetpoint>(attitude_setpoint_topic_, qos);
		trajectory_reference_pub_ =
			create_publisher<px4_msgs::msg::TrajectorySetpoint>("/fmu/in/trajectory_setpoint", qos);
		vehicle_command_pub_ =
			create_publisher<px4_msgs::msg::VehicleCommand>("/fmu/in/vehicle_command", qos);
		disturbance_estimate_pub_ = create_publisher<geometry_msgs::msg::Vector3Stamped>(
			"/uav_control/estimated_disturbance_acceleration", qos);
		payload_correction_pub_ = create_publisher<geometry_msgs::msg::Vector3Stamped>(
			"/uav_control/payload_swing_correction", qos);
		vehicle_status_sub_ = create_subscription<px4_msgs::msg::VehicleStatus>(
			"/fmu/out/vehicle_status", qos,
			[this](px4_msgs::msg::VehicleStatus::SharedPtr msg) {
				armed_ = msg->arming_state == px4_msgs::msg::VehicleStatus::ARMING_STATE_ARMED;
				offboard_ = msg->nav_state == px4_msgs::msg::VehicleStatus::NAVIGATION_STATE_OFFBOARD;
				if (armed_ && offboard_ && !command_confirmed_) {
					command_confirmed_ = true;
					RCLCPP_INFO(get_logger(), "PX4 confirmed offboard mode and armed state");
				}
			});

		start_time_ = now();
		timer_ = create_wall_timer(20ms, std::bind(&GeometricFigure8Attitude::timer_callback, this));

		RCLCPP_INFO(
			get_logger(),
			"Geometric Figure-8 attitude prototype started: A=%.2f m omega=%.2f rad/s z=%.2f NED "
			"disturbance_gain=%.2f swing_kp=%.2f swing_kd=%.2f attitude_topic=%s",
			amplitude_, omega_, altitude_ned_, disturbance_observer_gain_, payload_swing_kp_, payload_swing_kd_,
			attitude_setpoint_topic_.c_str());
	}

private:
	rclcpp::TimerBase::SharedPtr timer_;
	rclcpp::Subscription<px4_msgs::msg::VehicleLocalPosition>::SharedPtr local_position_sub_;
	rclcpp::Subscription<geometry_msgs::msg::Vector3Stamped>::SharedPtr payload_direction_sub_;
	rclcpp::Subscription<geometry_msgs::msg::Vector3Stamped>::SharedPtr payload_direction_rate_sub_;
	rclcpp::Publisher<px4_msgs::msg::OffboardControlMode>::SharedPtr offboard_control_mode_pub_;
	rclcpp::Publisher<px4_msgs::msg::VehicleAttitudeSetpoint>::SharedPtr attitude_setpoint_pub_;
	rclcpp::Publisher<px4_msgs::msg::TrajectorySetpoint>::SharedPtr trajectory_reference_pub_;
	rclcpp::Publisher<px4_msgs::msg::VehicleCommand>::SharedPtr vehicle_command_pub_;
	rclcpp::Publisher<geometry_msgs::msg::Vector3Stamped>::SharedPtr disturbance_estimate_pub_;
	rclcpp::Publisher<geometry_msgs::msg::Vector3Stamped>::SharedPtr payload_correction_pub_;
	rclcpp::Subscription<px4_msgs::msg::VehicleStatus>::SharedPtr vehicle_status_sub_;

	rclcpp::Time start_time_;
	Vec3 position_{};
	Vec3 velocity_{};
	Vec3 position_error_integral_{};
	Vec3 measured_acceleration_{};
	Vec3 previous_applied_acceleration_{};
	Vec3 disturbance_estimate_{};
	Vec3 payload_cable_direction_{};
	Vec3 payload_cable_direction_rate_{};
	bool have_position_{false};
	bool have_acceleration_{false};
	bool have_payload_direction_{false};
	int64_t payload_state_time_ns_{0};
	double amplitude_{5.0};
	double omega_{0.25};
	double altitude_ned_{-5.0};
	double kp_xy_{1.4};
	double kp_z_{2.2};
	double kd_xy_{1.1};
	double kd_z_{1.4};
	double ki_xy_{0.0};
	double ki_z_{0.0};
	double integral_limit_xy_{5.0};
	double integral_limit_z_{2.0};
	double integrator_leak_rate_{0.02};
	double max_tilt_deg_{35.0};
	double disturbance_observer_gain_{0.0};
	double disturbance_filter_hz_{0.5};
	double disturbance_limit_xy_{3.0};
	double payload_swing_kp_{0.0};
	double payload_swing_kd_{0.0};
	double payload_correction_limit_xy_{2.0};
	double payload_state_timeout_s_{0.15};
	double hover_thrust_{0.72};
	double min_thrust_{0.15};
	double max_thrust_{0.90};
	double takeoff_ramp_s_{8.0};
	std::string attitude_setpoint_topic_{"/fmu/in/vehicle_attitude_setpoint"};
	int arm_after_setpoints_{50};
	int setpoint_counter_{0};
	bool armed_{false};
	bool offboard_{false};
	bool command_confirmed_{false};
	bool control_saturated_{false};

	uint64_t timestamp_us() const
	{
		return now().nanoseconds() / 1000;
	}

	void local_position_callback(const px4_msgs::msg::VehicleLocalPosition::SharedPtr msg)
	{
		if (!msg->xy_valid || !msg->z_valid || !msg->v_xy_valid || !msg->v_z_valid) {
			return;
		}
		position_ = {msg->x, msg->y, msg->z};
		velocity_ = {msg->vx, msg->vy, msg->vz};
		if (std::isfinite(msg->ax) && std::isfinite(msg->ay) && std::isfinite(msg->az)) {
			measured_acceleration_ = {msg->ax, msg->ay, msg->az};
			have_acceleration_ = true;
		}
		have_position_ = true;
	}

	void publish_control_vector(
		const rclcpp::Publisher<geometry_msgs::msg::Vector3Stamped>::SharedPtr & publisher,
		const Vec3 & value)
	{
		geometry_msgs::msg::Vector3Stamped msg{};
		msg.header.stamp = now();
		msg.header.frame_id = "local_ned";
		msg.vector.x = value.x;
		msg.vector.y = value.y;
		msg.vector.z = value.z;
		publisher->publish(msg);
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
		msg.position = false;
		msg.velocity = false;
		msg.acceleration = false;
		msg.attitude = true;
		msg.body_rate = false;
		msg.timestamp = timestamp_us();
		offboard_control_mode_pub_->publish(msg);
	}

	void desired_reference(double t, Vec3 & xd, Vec3 & vd, Vec3 & ad) const
	{
		if (t < takeoff_ramp_s_) {
			const double s = std::max(0.0, std::min(1.0, t / takeoff_ramp_s_));
			const double smooth = s * s * (3.0 - 2.0 * s);
			const double smooth_dot = 6.0 * s * (1.0 - s) / takeoff_ramp_s_;
			const double smooth_ddot = 6.0 * (1.0 - 2.0 * s) / (takeoff_ramp_s_ * takeoff_ramp_s_);
			xd = {0.0, 0.0, altitude_ned_ * smooth};
			vd = {0.0, 0.0, altitude_ned_ * smooth_dot};
			ad = {0.0, 0.0, altitude_ned_ * smooth_ddot};
			return;
		}

		const double tau = t - takeoff_ramp_s_;
		const double phase = omega_ * tau;
		const double sin_phase = std::sin(phase);
		const double cos_phase = std::cos(phase);
		const double sin_2phase = std::sin(2.0 * phase);
		const double cos_2phase = std::cos(2.0 * phase);

		xd = {
			amplitude_ * sin_phase,
			0.5 * amplitude_ * sin_2phase,
			altitude_ned_,
		};
		vd = {
			amplitude_ * omega_ * cos_phase,
			amplitude_ * omega_ * cos_2phase,
			0.0,
		};
		ad = {
			-amplitude_ * omega_ * omega_ * sin_phase,
			-2.0 * amplitude_ * omega_ * omega_ * sin_2phase,
			0.0,
		};
	}

	void publish_reference(const Vec3 & xd, const Vec3 & vd)
	{
		px4_msgs::msg::TrajectorySetpoint msg{};
		msg.position = {
			static_cast<float>(xd.x),
			static_cast<float>(xd.y),
			static_cast<float>(xd.z),
		};
		msg.velocity = {
			static_cast<float>(vd.x),
			static_cast<float>(vd.y),
			static_cast<float>(vd.z),
		};
		msg.yaw = 0.0F;
		msg.timestamp = timestamp_us();
		trajectory_reference_pub_->publish(msg);
	}

	void publish_attitude_setpoint(const Vec3 & xd, const Vec3 & vd, const Vec3 & ad, double t)
	{
		if (!have_position_) {
			return;
		}

		const Vec3 e_p = position_ - xd;
		const Vec3 e_v = velocity_ - vd;
		const bool control_active = command_confirmed_ && t >= takeoff_ramp_s_;
		const bool integration_enabled = control_active && !control_saturated_;
		position_error_integral_ = uav_control::update_bounded_integral(
			position_error_integral_, e_p, 0.02, integrator_leak_rate_,
			integral_limit_xy_, integral_limit_z_, integration_enabled);

		const Vec3 base_acceleration = {
			ad.x - kp_xy_ * e_p.x - kd_xy_ * e_v.x - ki_xy_ * position_error_integral_.x,
			ad.y - kp_xy_ * e_p.y - kd_xy_ * e_v.y - ki_xy_ * position_error_integral_.y,
			ad.z - kp_z_ * e_p.z - kd_z_ * e_v.z - ki_z_ * position_error_integral_.z,
		};
		const bool disturbance_enabled =
			control_active && have_acceleration_ && disturbance_observer_gain_ > 0.0;
		disturbance_estimate_ = uav_control::update_disturbance_estimate(
			disturbance_estimate_, measured_acceleration_, previous_applied_acceleration_, 0.02,
			disturbance_filter_hz_, disturbance_limit_xy_, disturbance_enabled);

		const double payload_age_s = payload_state_time_ns_ > 0 ?
			static_cast<double>(now().nanoseconds() - payload_state_time_ns_) * 1e-9 : 1e9;
		const bool payload_feedback_enabled =
			control_active && have_payload_direction_ && payload_age_s >= 0.0 &&
			payload_age_s <= payload_state_timeout_s_ &&
			(payload_swing_kp_ > 0.0 || payload_swing_kd_ > 0.0);
		const Vec3 payload_correction = uav_control::payload_swing_correction(
			payload_cable_direction_, payload_cable_direction_rate_, payload_swing_kp_, payload_swing_kd_,
			payload_correction_limit_xy_, payload_feedback_enabled);

		const Vec3 unconstrained_acceleration = {
			base_acceleration.x - disturbance_observer_gain_ * disturbance_estimate_.x + payload_correction.x,
			base_acceleration.y - disturbance_observer_gain_ * disturbance_estimate_.y + payload_correction.y,
			base_acceleration.z,
		};
		bool tilt_saturated = false;
		const double max_tilt_rad = max_tilt_deg_ * std::acos(-1.0) / 180.0;
		const Vec3 a_cmd = uav_control::apply_tilt_limit(
			unconstrained_acceleration, kGravity, max_tilt_rad, tilt_saturated);
		previous_applied_acceleration_ = a_cmd;
		publish_control_vector(disturbance_estimate_pub_, disturbance_estimate_);
		publish_control_vector(payload_correction_pub_, payload_correction);

		const Vec3 desired_body_z_down = normalized({-a_cmd.x, -a_cmd.y, kGravity - a_cmd.z}, {0.0, 0.0, 1.0});
		const Vec3 yaw_reference = {1.0, 0.0, 0.0};
		const Vec3 body_y = normalized(cross(desired_body_z_down, yaw_reference), {0.0, 1.0, 0.0});
		const Vec3 body_x = normalized(cross(body_y, desired_body_z_down), {1.0, 0.0, 0.0});
		const Quat q = rotation_matrix_to_quaternion(body_x, body_y, desired_body_z_down);

		const double raw_collective =
			hover_thrust_ * norm({a_cmd.x, a_cmd.y, kGravity - a_cmd.z}) / kGravity;
		const double collective = clamp(raw_collective, min_thrust_, max_thrust_);
		control_saturated_ = tilt_saturated || raw_collective < min_thrust_ || raw_collective > max_thrust_;

		px4_msgs::msg::VehicleAttitudeSetpoint msg{};
		msg.q_d = {
			static_cast<float>(q.w),
			static_cast<float>(q.x),
			static_cast<float>(q.y),
			static_cast<float>(q.z),
		};
		msg.yaw_sp_move_rate = 0.0F;
		msg.thrust_body = {0.0F, 0.0F, static_cast<float>(-collective)};
		msg.timestamp = timestamp_us();
		attitude_setpoint_pub_->publish(msg);
	}

	void timer_callback()
	{
		const double t = (now() - start_time_).seconds();
		Vec3 xd{};
		Vec3 vd{};
		Vec3 ad{};
		desired_reference(t, xd, vd, ad);

		publish_offboard_control_mode();
		publish_reference(xd, vd);
		publish_attitude_setpoint(xd, vd, ad, t);

		if (!command_confirmed_ && setpoint_counter_ >= arm_after_setpoints_ &&
			setpoint_counter_ % 50 == 0)
		{
			if (!offboard_) {
				publish_vehicle_command(px4_msgs::msg::VehicleCommand::VEHICLE_CMD_DO_SET_MODE, 1.0F, 6.0F);
			}
			if (!armed_) {
				publish_vehicle_command(px4_msgs::msg::VehicleCommand::VEHICLE_CMD_COMPONENT_ARM_DISARM, 1.0F);
			}
			RCLCPP_INFO(get_logger(), "Requested offboard mode and arm; awaiting PX4 confirmation");
		}

		++setpoint_counter_;
	}
};

int main(int argc, char * argv[])
{
	rclcpp::init(argc, argv);
	rclcpp::spin(std::make_shared<GeometricFigure8Attitude>());
	rclcpp::shutdown();
	return 0;
}
