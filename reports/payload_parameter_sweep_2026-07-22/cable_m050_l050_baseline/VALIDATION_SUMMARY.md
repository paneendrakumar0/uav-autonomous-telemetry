# Single Validation Run

**Created**: 2026-07-25T10:31:21
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

- `samples`: `3720`
- `duration_s`: `74.3796`
- `mean_3d_error_m`: `0.4489`
- `rms_3d_error_m`: `0.4804`
- `max_3d_error_m`: `0.7106`
- `mean_xy_error_m`: `0.4487`
- `mean_z_ned_m`: `-5.0001`
- `max_abs_position_m`: `5.3941`
- `mean_altitude_error_m`: `0.0001`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18573`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `0.5002`
- `mean_lateral_swing_m`: `0.2833`
- `max_lateral_swing_m`: `0.3618`
- `mean_cable_angle_deg`: `34.7595`
- `max_cable_angle_deg`: `46.3149`
- `profile`: `baseline`
- `launch_file`: `figure8_payload_experiment.launch.py`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `/home/paneendra/uav-autonomous-telemetry/reports/payload_parameter_sweep_2026-07-22/cable_m050_l050_baseline`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
