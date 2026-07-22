# Single Validation Run

**Created**: 2026-07-22T19:03:34
**Profile**: `baseline`
**Launch File**: `figure8_payload_experiment.launch.py`
**Flight Duration**: `75.0 s`
**Omega**: `0.3`
**Hover Thrust**: `0.72`

## Result

- Tracking valid: `True`
- Tracking reason: valid tracking telemetry
- Payload swing reason: valid payload swing telemetry

## Metrics

- `samples`: `3709`
- `duration_s`: `74.1641`
- `mean_3d_error_m`: `0.6772`
- `rms_3d_error_m`: `0.7201`
- `max_3d_error_m`: `1.0356`
- `mean_xy_error_m`: `0.6770`
- `mean_z_ned_m`: `-4.9971`
- `max_abs_position_m`: `5.6962`
- `mean_altitude_error_m`: `0.0029`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18539`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0016`
- `mean_lateral_swing_m`: `0.6564`
- `max_lateral_swing_m`: `0.8060`
- `mean_cable_angle_deg`: `41.3792`
- `max_cable_angle_deg`: `53.5126`
- `profile`: `baseline`
- `launch_file`: `figure8_payload_experiment.launch.py`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `reports/speed_sweep_validation_2026-07-22/omega_030/baseline_trial_03`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
