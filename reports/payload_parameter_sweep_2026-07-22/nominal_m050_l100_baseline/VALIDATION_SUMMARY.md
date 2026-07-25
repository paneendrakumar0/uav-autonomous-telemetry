# Single Validation Run

**Created**: 2026-07-22T19:31:46
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
- `duration_s`: `74.1476`
- `mean_3d_error_m`: `0.4458`
- `rms_3d_error_m`: `0.4755`
- `max_3d_error_m`: `0.6665`
- `mean_xy_error_m`: `0.4453`
- `mean_z_ned_m`: `-4.9983`
- `max_abs_position_m`: `5.4173`
- `mean_altitude_error_m`: `0.0017`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18500`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0013`
- `mean_lateral_swing_m`: `0.5631`
- `max_lateral_swing_m`: `0.7296`
- `mean_cable_angle_deg`: `34.5050`
- `max_cable_angle_deg`: `46.7198`
- `profile`: `baseline`
- `launch_file`: `figure8_payload_experiment.launch.py`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `/home/paneendra/uav-autonomous-telemetry/reports/payload_parameter_sweep_2026-07-22/nominal_m050_l100_baseline`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
