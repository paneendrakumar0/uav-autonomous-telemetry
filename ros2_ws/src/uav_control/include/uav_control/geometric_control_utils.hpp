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

	const double xy_norm = std::hypot(next.x, next.y);
	if (xy_limit > 0.0 && xy_norm > xy_limit) {
		const double scale = xy_limit / xy_norm;
		next.x *= scale;
		next.y *= scale;
	}
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
