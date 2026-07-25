# Single Validation Run

**Created**: 2026-07-25T10:27:36
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

- `samples`: `3707`
- `duration_s`: `74.1249`
- `mean_3d_error_m`: `0.5908`
- `rms_3d_error_m`: `0.6266`
- `max_3d_error_m`: `0.8557`
- `mean_xy_error_m`: `0.5906`
- `mean_z_ned_m`: `-5.0003`
- `max_abs_position_m`: `5.4448`
- `mean_altitude_error_m`: `0.0003`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18488`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0013`
- `mean_lateral_swing_m`: `0.5633`
- `max_lateral_swing_m`: `0.7225`
- `mean_cable_angle_deg`: `34.4996`
- `max_cable_angle_deg`: `46.1338`
- `profile`: `baseline`
- `launch_file`: `figure8_payload_experiment.launch.py`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `/home/paneendra/uav-autonomous-telemetry/reports/payload_parameter_sweep_2026-07-22/mass_m200_l100_baseline`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
