# Single Validation Run

**Created**: 2026-07-22T18:27:05
**Profile**: `baseline`
**Launch File**: `figure8_payload_experiment.launch.py`
**Flight Duration**: `75.0 s`
**Omega**: `0.15`
**Hover Thrust**: `0.72`

## Result

- Tracking valid: `True`
- Tracking reason: valid tracking telemetry
- Payload swing reason: valid payload swing telemetry

## Metrics

- `samples`: `3722`
- `duration_s`: `74.4274`
- `mean_3d_error_m`: `0.1785`
- `rms_3d_error_m`: `0.1908`
- `max_3d_error_m`: `0.3095`
- `mean_xy_error_m`: `0.1768`
- `mean_z_ned_m`: `-5.0009`
- `max_abs_position_m`: `5.1894`
- `mean_altitude_error_m`: `0.0009`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18578`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0005`
- `mean_lateral_swing_m`: `0.3546`
- `max_lateral_swing_m`: `0.5045`
- `mean_cable_angle_deg`: `20.8412`
- `max_cable_angle_deg`: `30.2650`
- `profile`: `baseline`
- `launch_file`: `figure8_payload_experiment.launch.py`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `reports/speed_sweep_validation_2026-07-22/omega_015/baseline_trial_01`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
