#pragma once

#include <algorithm>
#include <cmath>

namespace uav_control
{
struct Vector3
{
	double x{0.0};
	double y{0.0};
	double z{0.0};
};

inline Vector3 clamp_horizontal_norm(const Vector3 & value, double limit)
{
	Vector3 limited = value;
	const double horizontal_norm = std::hypot(limited.x, limited.y);
	if (limit > 0.0 && horizontal_norm > limit) {
		const double scale = limit / horizontal_norm;
		limited.x *= scale;
		limited.y *= scale;
	}
	return limited;
}

inline Vector3 update_disturbance_estimate(
	const Vector3 & previous_estimate,
	const Vector3 & measured_acceleration,
	const Vector3 & previous_applied_acceleration,
	double dt_s,
	double cutoff_hz,
	double horizontal_limit,
	bool enabled)
{
	if (!enabled || dt_s <= 0.0 || cutoff_hz <= 0.0) {
		return {};
	}
	const double alpha = 1.0 - std::exp(-2.0 * std::acos(-1.0) * cutoff_hz * dt_s);
	const Vector3 raw{
		measured_acceleration.x - previous_applied_acceleration.x,
		measured_acceleration.y - previous_applied_acceleration.y,
		0.0,
	};
	return clamp_horizontal_norm(
		{
			previous_estimate.x + alpha * (raw.x - previous_estimate.x),
			previous_estimate.y + alpha * (raw.y - previous_estimate.y),
			0.0,
		},
		horizontal_limit);
}

inline Vector3 payload_swing_correction(
	const Vector3 & cable_direction_ned,
	const Vector3 & cable_direction_rate_ned,
	double proportional_gain,
	double derivative_gain,
	double horizontal_limit,
	bool enabled)
{
	if (!enabled) {
		return {};
	}
	return clamp_horizontal_norm(
		{
			proportional_gain * cable_direction_ned.x + derivative_gain * cable_direction_rate_ned.x,
			proportional_gain * cable_direction_ned.y + derivative_gain * cable_direction_rate_ned.y,
			0.0,
		},
		horizontal_limit);
}

inline Vector3 update_bounded_integral(
	const Vector3 & state,
	const Vector3 & error,
	double dt_s,
	double leak_rate_hz,
	double xy_limit,
	double z_limit,
	bool integration_enabled)
{
	const double decay = std::max(0.0, 1.0 - std::max(0.0, leak_rate_hz) * dt_s);
	Vector3 next{decay * state.x, decay * state.y, decay * state.z};
	if (integration_enabled) {
		next.x += dt_s * error.x;
		next.y += dt_s * error.y;
		next.z += dt_s * error.z;
	}

	next = clamp_horizontal_norm(next, xy_limit);
	next.z = std::clamp(next.z, -std::max(0.0, z_limit), std::max(0.0, z_limit));
	return next;
}

inline Vector3 apply_tilt_limit(
	const Vector3 & acceleration_command,
	double gravity,
	double max_tilt_rad,
	bool & saturated)
{
	Vector3 limited = acceleration_command;
	const double lateral = std::hypot(limited.x, limited.y);
	const double vertical_thrust_accel = std::max(0.1, gravity - limited.z);
	const double lateral_limit = vertical_thrust_accel * std::tan(std::max(0.0, max_tilt_rad));
	saturated = lateral > lateral_limit;
	if (saturated && lateral > 1e-9) {
		const double scale = lateral_limit / lateral;
		limited.x *= scale;
		limited.y *= scale;
	}
	return limited;
}
}  // namespace uav_control
