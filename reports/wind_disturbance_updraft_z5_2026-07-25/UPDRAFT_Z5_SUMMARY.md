# Vertical Updraft Validation - 2026-07-25

## Purpose

This phase tests vertical disturbance sensitivity after the horizontal crosswind and gust experiments. The objective is to stress altitude control and check whether the controllers can still execute the Figure-8 circuit under a strong vertical wind component.

## Setup

- Vehicle: `iris_depth_payload`
- Payload: nominal `0.05 kg`, `1.0 m` cable
- Trajectory: Figure-8
- Angular rate: `0.25 rad/s`
- Wind world: `payload_updraft_z5`
- Wind model: Gazebo Classic `libgazebo_wind_plugin.so`
- Wind velocity: constant `5.0 m/s`
- Wind direction: `0 0 1`, Gazebo +Z direction
- Controllers: PX4 position/velocity baseline and tuned geometric attitude/thrust controller
- Trials: `1` baseline + `1` geometric screening trial

## Results

| Metric | PX4 baseline | Geometric |
| --- | ---: | ---: |
| Tracking valid | `false` | `true` |
| Mean 3D tracking error | `6.3698 m` | `0.8452 m` |
| RMS 3D tracking error | `6.4120 m` | `0.8514 m` |
| Max 3D tracking error | `7.1165 m` | `1.1419 m` |
| Mean altitude, NED | `0.0173 m` | `-4.4410 m` |
| Mean altitude error | `5.0173 m` | `0.5590 m` |
| Mean lateral swing | `0.0000 m` | `0.5214 m` |
| Mean cable angle | `0.0018 deg` | `31.6028 deg` |

## Evidence

- Baseline summary: `baseline_updraft_z5/VALIDATION_SUMMARY.md`
- Geometric summary: `geometric_updraft_z5/VALIDATION_SUMMARY.md`
- Baseline plots: `baseline_updraft_z5/validation_*.png`
- Geometric plots: `geometric_updraft_z5/validation_*.png`
- Comparison CSV: `updraft_z5_controller_comparison.csv`

## Interpretation

The vertical updraft exposes a hard failure boundary for the PX4 baseline in this setup. The baseline trial did not reach the commanded `-5 m` NED altitude and failed the altitude validation gate with a mean altitude error of `5.0173 m`.

The geometric controller completed the circuit and passed validation, but it still flew above the target altitude with a mean altitude error of `0.5590 m`. This confirms that the geometric controller is more robust than the PX4 baseline under this vertical disturbance, but the altitude/thrust channel is not fully disturbance compensated.

The baseline payload swing values are not physically comparable to the geometric swing values because the baseline vehicle did not execute the Figure-8 circuit. This test should be treated as a failure-boundary result, not a normal controller-improvement percentage comparison.
