# Single Validation Run

**Created**: 2026-07-21T20:06:26
**Profile**: `baseline`
**Launch File**: `figure8_payload_experiment.launch.py`
**Flight Duration**: `75.0 s`
**Omega**: `0.25`
**Hover Thrust**: `0.72`

## Result

- Tracking valid: `True`
- Tracking reason: valid tracking telemetry
- Payload swing reason: valid payload swing telemetry

## Metrics

- `samples`: `3708`
- `duration_s`: `74.1481`
- `mean_3d_error_m`: `0.4413`
- `rms_3d_error_m`: `0.4718`
- `max_3d_error_m`: `0.6672`
- `mean_xy_error_m`: `0.4409`
- `mean_z_ned_m`: `-4.9987`
- `max_abs_position_m`: `5.3861`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18538`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0012`
- `mean_lateral_swing_m`: `0.5636`
- `max_lateral_swing_m`: `0.7301`
- `mean_cable_angle_deg`: `34.5455`
- `max_cable_angle_deg`: `46.7719`
- `profile`: `baseline`
- `launch_file`: `figure8_payload_experiment.launch.py`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `reports/single_validation_2026-07-21_baseline_june12`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
