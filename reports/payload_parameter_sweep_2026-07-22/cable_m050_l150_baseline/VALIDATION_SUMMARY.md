# Single Validation Run

**Created**: 2026-07-25T10:35:06
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

- `samples`: `3723`
- `duration_s`: `74.4444`
- `mean_3d_error_m`: `0.4334`
- `rms_3d_error_m`: `0.4635`
- `max_3d_error_m`: `0.6894`
- `mean_xy_error_m`: `0.4331`
- `mean_z_ned_m`: `-5.0009`
- `max_abs_position_m`: `5.3768`
- `mean_altitude_error_m`: `0.0009`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18587`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.5032`
- `mean_lateral_swing_m`: `0.8436`
- `max_lateral_swing_m`: `1.0826`
- `mean_cable_angle_deg`: `34.3972`
- `max_cable_angle_deg`: `45.9967`
- `profile`: `baseline`
- `launch_file`: `figure8_payload_experiment.launch.py`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `/home/paneendra/uav-autonomous-telemetry/reports/payload_parameter_sweep_2026-07-22/cable_m050_l150_baseline`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
