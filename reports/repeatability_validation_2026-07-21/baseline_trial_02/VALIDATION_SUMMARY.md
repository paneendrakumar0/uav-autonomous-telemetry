# Single Validation Run

**Created**: 2026-07-21T20:15:40
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
- `duration_s`: `74.1482`
- `mean_3d_error_m`: `0.4448`
- `rms_3d_error_m`: `0.4755`
- `max_3d_error_m`: `0.6728`
- `mean_xy_error_m`: `0.4444`
- `mean_z_ned_m`: `-4.9988`
- `max_abs_position_m`: `5.3909`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18537`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0012`
- `mean_lateral_swing_m`: `0.5642`
- `max_lateral_swing_m`: `0.7310`
- `mean_cable_angle_deg`: `34.5834`
- `max_cable_angle_deg`: `46.8469`
- `profile`: `baseline`
- `launch_file`: `figure8_payload_experiment.launch.py`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `reports/repeatability_validation_2026-07-21/baseline_trial_02`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
