# Single Validation Run

**Created**: 2026-07-22T17:41:11
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

- `samples`: `3709`
- `duration_s`: `74.1650`
- `mean_3d_error_m`: `0.4451`
- `rms_3d_error_m`: `0.4751`
- `max_3d_error_m`: `0.6668`
- `mean_xy_error_m`: `0.4447`
- `mean_z_ned_m`: `-4.9988`
- `max_abs_position_m`: `5.4101`
- `mean_altitude_error_m`: `0.0012`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18417`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0012`
- `mean_lateral_swing_m`: `0.5622`
- `max_lateral_swing_m`: `0.7317`
- `mean_cable_angle_deg`: `34.4427`
- `max_cable_angle_deg`: `46.9032`
- `profile`: `baseline`
- `launch_file`: `figure8_payload_experiment.launch.py`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `reports/repeatability_validation_10x10_2026-07-22/baseline_trial_01`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
