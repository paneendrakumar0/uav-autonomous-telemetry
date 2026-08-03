#include <gtest/gtest.h>

#include <cmath>

#include "uav_control/geometric_control_utils.hpp"

TEST(GeometricControlUtils, BoundsIntegralByHorizontalNormAndVerticalLimit)
{
	const uav_control::Vector3 state{};
	const uav_control::Vector3 error{10.0, 10.0, 10.0};
	const auto result = uav_control::update_bounded_integral(state, error, 1.0, 0.0, 2.0, 1.0, true);
	EXPECT_NEAR(std::hypot(result.x, result.y), 2.0, 1e-9);
	EXPECT_DOUBLE_EQ(result.z, 1.0);
}

TEST(GeometricControlUtils, LeaksButDoesNotIntegrateWhenDisabled)
{
	const uav_control::Vector3 state{2.0, -1.0, 0.5};
	const uav_control::Vector3 error{100.0, 100.0, 100.0};
	const auto result = uav_control::update_bounded_integral(state, error, 0.5, 0.2, 10.0, 10.0, false);
	EXPECT_DOUBLE_EQ(result.x, 1.8);
	EXPECT_DOUBLE_EQ(result.y, -0.9);
	EXPECT_DOUBLE_EQ(result.z, 0.45);
}

TEST(GeometricControlUtils, EnforcesTiltLimitWithoutChangingVerticalCommand)
{
	const uav_control::Vector3 command{20.0, 0.0, 0.0};
	bool saturated = false;
	const auto result = uav_control::apply_tilt_limit(command, 9.80665, 30.0 * std::acos(-1.0) / 180.0, saturated);
	EXPECT_TRUE(saturated);
	EXPECT_NEAR(result.x, 9.80665 * std::tan(30.0 * std::acos(-1.0) / 180.0), 1e-9);
	EXPECT_DOUBLE_EQ(result.y, 0.0);
	EXPECT_DOUBLE_EQ(result.z, 0.0);
}

TEST(GeometricControlUtils, LeavesFeasibleAccelerationUnchanged)
{
	const uav_control::Vector3 command{1.0, -1.0, 0.2};
	bool saturated = false;
	const auto result = uav_control::apply_tilt_limit(command, 9.80665, 35.0 * std::acos(-1.0) / 180.0, saturated);
	EXPECT_FALSE(saturated);
	EXPECT_DOUBLE_EQ(result.x, command.x);
	EXPECT_DOUBLE_EQ(result.y, command.y);
	EXPECT_DOUBLE_EQ(result.z, command.z);
}

TEST(GeometricControlUtils, FiltersAndBoundsHorizontalDisturbanceEstimate)
{
	const uav_control::Vector3 previous{};
	const uav_control::Vector3 measured{10.0, 0.0, 5.0};
	const uav_control::Vector3 applied{};
	const auto result = uav_control::update_disturbance_estimate(
		previous, measured, applied, 1.0, 10.0, 2.0, true);
	EXPECT_NEAR(result.x, 2.0, 1e-9);
	EXPECT_DOUBLE_EQ(result.y, 0.0);
	EXPECT_DOUBLE_EQ(result.z, 0.0);
}

TEST(GeometricControlUtils, ClearsDisturbanceEstimateWhenDisabled)
{
	const auto result = uav_control::update_disturbance_estimate(
		{1.0, -2.0, 0.0}, {5.0, 5.0, 0.0}, {0.0, 0.0, 0.0}, 0.02, 0.5, 3.0, false);
	EXPECT_DOUBLE_EQ(result.x, 0.0);
	EXPECT_DOUBLE_EQ(result.y, 0.0);
	EXPECT_DOUBLE_EQ(result.z, 0.0);
}

TEST(GeometricControlUtils, ComputesBoundedPayloadSwingCorrection)
{
	const auto result = uav_control::payload_swing_correction(
		{0.6, 0.8, 0.0}, {0.0, 0.0, 0.0}, 2.0, 0.0, 1.0, true);
	EXPECT_NEAR(result.x, 0.6, 1e-9);
	EXPECT_NEAR(result.y, 0.8, 1e-9);
	EXPECT_DOUBLE_EQ(result.z, 0.0);
}

TEST(GeometricControlUtils, DisablesPayloadSwingCorrectionExplicitly)
{
	const auto result = uav_control::payload_swing_correction(
		{1.0, 1.0, 0.0}, {1.0, 1.0, 0.0}, 5.0, 5.0, 1.0, false);
	EXPECT_DOUBLE_EQ(result.x, 0.0);
	EXPECT_DOUBLE_EQ(result.y, 0.0);
}
