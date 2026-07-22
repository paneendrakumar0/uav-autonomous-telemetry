# Single Validation Run

**Created**: 2026-07-22T19:07:13
**Profile**: `geometric`
**Launch File**: `geometric_figure8_experiment.launch.py`
**Flight Duration**: `75.0 s`
**Omega**: `0.3`
**Hover Thrust**: `0.72`

## Result

- Tracking valid: `True`
- Tracking reason: valid tracking telemetry
- Payload swing reason: valid payload swing telemetry

## Metrics

- `samples`: `3722`
- `duration_s`: `74.4196`
- `mean_3d_error_m`: `0.3833`
- `rms_3d_error_m`: `0.3999`
- `max_3d_error_m`: `0.6487`
- `mean_xy_error_m`: `0.3831`
- `mean_z_ned_m`: `-4.9983`
- `max_abs_position_m`: `5.0237`
- `mean_altitude_error_m`: `0.0017`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18580`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0013`
- `mean_lateral_swing_m`: `0.5854`
- `max_lateral_swing_m`: `0.7444`
- `mean_cable_angle_deg`: `36.0724`
- `max_cable_angle_deg`: `47.9759`
- `profile`: `geometric`
- `launch_file`: `geometric_figure8_experiment.launch.py`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `reports/speed_sweep_validation_2026-07-22/omega_030/geometric_trial_02`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
