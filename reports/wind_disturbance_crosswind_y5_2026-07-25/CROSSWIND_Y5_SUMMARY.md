# Constant Crosswind Validation - 2026-07-25

## Purpose

This phase introduces a controlled aerodynamic disturbance after the clean-air speed and payload-parameter sweeps. The test checks whether the PX4 baseline and tuned geometric controller remain effective under a constant horizontal crosswind.

## Setup

- Vehicle: `iris_depth_payload`
- Payload: nominal `0.05 kg`, `1.0 m` cable
- Trajectory: Figure-8
- Angular rate: `0.25 rad/s`
- Wind world: `payload_crosswind_y5`
- Wind model: Gazebo Classic `libgazebo_wind_plugin.so`
- Wind velocity: constant `5.0 m/s`
- Wind direction: `0 1 0`, positive Y direction
- Controllers: PX4 position/velocity baseline and tuned geometric attitude/thrust controller
- Trials: `1` baseline + `1` geometric screening trial

## Metrics

| Metric | PX4 baseline | Geometric | Geometric improvement |
| --- | ---: | ---: | ---: |
| Mean 3D tracking error | `0.4467 m` | `1.2690 m` | `-184.08%` |
| RMS 3D tracking error | `0.4782 m` | `1.3013 m` | `-172.11%` |
| Mean lateral swing | `0.5662 m` | `0.5139 m` | `9.23%` |
| Mean cable angle | `34.7045 deg` | `31.0788 deg` | `10.45%` |

## Evidence

- Baseline summary: `baseline_crosswind_y5/VALIDATION_SUMMARY.md`
- Geometric summary: `geometric_crosswind_y5/VALIDATION_SUMMARY.md`
- Baseline plots: `baseline_crosswind_y5/validation_*.png`
- Geometric plots: `geometric_crosswind_y5/validation_*.png`
- Comparison CSV: `crosswind_y5_controller_comparison.csv`

## Interpretation

Both controllers completed the Figure-8 circuit and passed the validation gates under constant `5 m/s` Y-crosswind.

The result exposes an important limitation of the current geometric-controller tuning. The geometric controller still reduces payload swing and cable angle by roughly `9-10%`, but its trajectory tracking becomes much worse than the PX4 baseline under constant crosswind. The mean 3D tracking error rises from `0.4467 m` for the PX4 baseline to `1.2690 m` for the geometric controller.

This supports the current research direction: the geometric controller is useful for swing reduction, but it needs wind-aware or disturbance-aware compensation before it can be claimed as robust under external aerodynamic disturbances.
