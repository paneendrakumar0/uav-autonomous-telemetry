# Single Validation Run

**Created**: 2026-07-22T17:52:08
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

- `samples`: `3710`
- `duration_s`: `74.1793`
- `mean_3d_error_m`: `0.4458`
- `rms_3d_error_m`: `0.4763`
- `max_3d_error_m`: `0.6746`
- `mean_xy_error_m`: `0.4455`
- `mean_z_ned_m`: `-4.9989`
- `max_abs_position_m`: `5.3892`
- `mean_altitude_error_m`: `0.0011`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18545`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0012`
- `mean_lateral_swing_m`: `0.5645`
- `max_lateral_swing_m`: `0.7310`
- `mean_cable_angle_deg`: `34.6058`
- `max_cable_angle_deg`: `46.8433`
- `profile`: `baseline`
- `launch_file`: `figure8_payload_experiment.launch.py`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `reports/repeatability_validation_10x10_2026-07-22/baseline_trial_07`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
