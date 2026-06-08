# Next Stage Controller Roadmap - 2026-06-08

## Goal

Move the project from validated PX4 offboard trajectory following toward a controller experiment that can answer a stronger research question:

> Can the UAV track the requested Figure-8 path while reducing payload swing, rather than only tolerating it?

The present repository already proves the simulation stack, physical payload model, telemetry logging, and Figure-8 baseline. The next stage should therefore focus on a controlled comparison between the current PX4 position/velocity setpoint baseline and a more explicit control layer inspired by geometric quadrotor control.

## Current Baseline

The current controller publishes PX4 `TrajectorySetpoint` messages containing position and velocity references:

- Path: lemniscate/Figure-8
- Amplitude: `5.0 m`
- Angular rate: `0.25 rad/s`
- Altitude: `-5.0 m` NED
- Payload: `0.05 kg` native internal ball-joint payload

Measured steady-state results:

- No-payload Figure-8 mean 3D error: `0.415 m`
- Payload Figure-8 mean 3D error: `0.462 m`
- Payload Figure-8 RMS 3D error: `0.493 m`
- Payload Figure-8 maximum 3D error: `0.796 m`

This is the correct baseline to show Professor Zavoli before changing the controller, because it proves the requested 8-shaped circuit is complete with the slung payload attached.

## Stage 1: Fix Payload State Estimation

Before claiming payload swing reduction, the payload telemetry must be made frame-consistent.

Tasks:

- Replace the UDP pose-sniffer interpretation with an explicit Gazebo model/link-state reader where available.
- Confirm the reported cable length remains close to the known physical length during hover.
- Calibrate `base_link -> slung_payload` relative position using a static hover case.
- Regenerate hover and Figure-8 swing plots after the frame check.

Acceptance criteria:

- Hover cable length estimate stays approximately constant.
- Hover cable angle is small after transients.
- Figure-8 swing metrics are repeatable across at least three runs.

## Stage 2: Add Controller Comparison Harness

Keep the present controller as `baseline_position_velocity`. Add a launch-level experiment switch so the same trajectory, duration, payload model, and logger can be reused for later controllers.

Suggested experiment cases:

| Case | Payload | Controller | Purpose |
| --- | --- | --- | --- |
| A | no | PX4 position/velocity | clean trajectory reference |
| B | yes | PX4 position/velocity | current payload baseline |
| C | yes | geometric attitude/thrust reference | controller upgrade |
| D | yes | payload-aware reference shaping | swing reduction test |

Acceptance criteria:

- Every case writes the same tracking CSV schema.
- Payload cases write the same swing CSV schema.
- The benchmark summary can be regenerated with one command.

## Stage 3: Geometric Controller Prototype

Professor Zavoli pointed to geometric control on SE(3) as the next controller direction. A practical first implementation can stay outside PX4 as a ROS 2 node:

- Input: desired position, velocity, acceleration, yaw, and current vehicle odometry.
- Compute desired total thrust direction from position and velocity errors.
- Convert desired attitude into PX4-compatible attitude/thrust setpoints.
- Start without payload compensation, then add payload-angle feedback once payload state estimation is reliable.

Implementation note:

PX4 offboard supports multiple reference levels. The current work uses position/velocity setpoints. The geometric-controller stage should be developed as a separate node so the proven baseline remains untouched and comparable.

## Stage 4: Payload-Aware Trajectory Tuning

Once the geometric-controller prototype is stable, test whether swing can be reduced by shaping the Figure-8 command:

- Reduce angular rate from `0.25 rad/s` to lower values and measure swing.
- Add smooth acceleration ramps before entering the steady Figure-8.
- Compare payload swing against tracking error to expose the trade-off between aggressive path following and pendulum excitation.
- Optionally add input shaping using the estimated pendulum natural frequency.

Primary metrics:

- Mean and RMS 3D path error
- Mean and maximum lateral payload swing
- Mean and maximum cable angle
- Settling time after trajectory start
- Repeatability over multiple runs

## Immediate Next Commit Target

The most useful next code commit is:

1. Add a reusable benchmark runner or script that executes the no-payload and payload Figure-8 runs with fixed parameters.
2. Regenerate the benchmark markdown automatically from CSV files.
3. Add the first geometric-controller ROS 2 node skeleton without replacing the existing working Figure-8 controller.

This keeps the project credible: the baseline remains reproducible, and the new controller work has a clean comparison target.
