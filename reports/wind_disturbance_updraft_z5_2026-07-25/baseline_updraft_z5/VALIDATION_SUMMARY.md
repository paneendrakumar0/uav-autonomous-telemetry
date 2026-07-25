# Single Validation Run

**Created**: 2026-07-25T11:04:12
**Profile**: `baseline`
**Launch File**: `figure8_payload_experiment.launch.py`
**World**: `payload_updraft_z5`
**Flight Duration**: `75.0 s`
**Omega**: `0.25`
**Hover Thrust**: `0.72`

## Result

- Tracking valid: `False`
- Tracking reason: mean altitude error too large (5.02 m > 1.50 m)
- Payload swing reason: valid payload swing telemetry

## Metrics

- `samples`: `3722`
- `duration_s`: `74.4282`
- `mean_3d_error_m`: `6.3698`
- `rms_3d_error_m`: `6.4120`
- `max_3d_error_m`: `7.1165`
- `mean_xy_error_m`: `3.7093`
- `mean_z_ned_m`: `0.0173`
- `max_abs_position_m`: `0.0798`
- `mean_altitude_error_m`: `5.0173`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18581`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0000`
- `mean_lateral_swing_m`: `0.0000`
- `max_lateral_swing_m`: `0.0001`
- `mean_cable_angle_deg`: `0.0018`
- `max_cable_angle_deg`: `0.0029`
- `profile`: `baseline`
- `launch_file`: `figure8_payload_experiment.launch.py`
- `world`: `payload_updraft_z5`
- `tracking_valid`: `False`
- `tracking_reason`: `mean altitude error too large (5.02 m > 1.50 m)`
- `output_dir`: `reports/wind_disturbance_updraft_z5_2026-07-25/baseline_updraft_z5`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
