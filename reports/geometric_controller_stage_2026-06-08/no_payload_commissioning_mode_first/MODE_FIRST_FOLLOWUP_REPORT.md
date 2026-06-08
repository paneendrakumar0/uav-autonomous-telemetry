# No-Payload Geometric Follow-Up Run - 2026-06-08

## Objective

Retest the geometric attitude/thrust prototype after changing the command order to request Offboard mode before arming.

## Setup

- Vehicle: `iris_depth_camera`
- Controller: `geometric_figure8_attitude`
- Command sequence: Offboard mode first, arm second
- Amplitude: `5.0 m`
- Angular rate: `0.20 rad/s`
- Target altitude: `-5.0 m` NED
- Hover thrust parameter: `0.75`

## Result

The vehicle still did not climb. The `trajectory_setpoint` topic was verified fresh inside PX4, while `vehicle_attitude_setpoint` remained stale in the PX4 listener. This indicates the current blocker is the attitude-setpoint ingestion path, not the Figure-8 reference generator and not payload dynamics.

## Metrics

- Samples: `2733`
- Duration: `54.65 s`
- Minimum actual Z NED: `-0.072 m`
- Maximum actual Z NED: `0.037 m`
- Final actual Z NED: `0.037 m`
- Post-12s mean 3D error: `6.393 m`
- Post-12s maximum 3D error: `7.100 m`

## Verified During Run

- PX4 `trajectory_setpoint` listener showed recent Figure-8 reference data.
- PX4 `vehicle_attitude_setpoint` listener showed stale data from an older timestamp.
- The no-payload vehicle remained near ground altitude, so no payload model was involved.

## Next Debug Step

Inspect the ROS 2 topic type/version and uXRCE-DDS reader creation for `/fmu/in/vehicle_attitude_setpoint`. If necessary, move the prototype to a split `vehicle_rates_setpoint` plus `vehicle_thrust_setpoint` interface, or use the PX4 ROS 2 control-interface library for attitude/thrust offboard transport.

## Artifacts

- `geometric_figure8_tracking_metrics.csv`
- `geometric_mode_first_altitude_error.png`
