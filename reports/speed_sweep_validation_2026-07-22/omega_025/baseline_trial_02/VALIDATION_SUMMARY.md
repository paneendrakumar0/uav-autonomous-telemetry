# Single Validation Run

**Created**: 2026-07-22T18:50:48
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

- `samples`: `3722`
- `duration_s`: `74.4206`
- `mean_3d_error_m`: `0.4458`
- `rms_3d_error_m`: `0.4755`
- `max_3d_error_m`: `0.6724`
- `mean_xy_error_m`: `0.4455`
- `mean_z_ned_m`: `-4.9984`
- `max_abs_position_m`: `5.3917`
- `mean_altitude_error_m`: `0.0016`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18586`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0012`
- `mean_lateral_swing_m`: `0.5639`
- `max_lateral_swing_m`: `0.7309`
- `mean_cable_angle_deg`: `34.5675`
- `max_cable_angle_deg`: `46.8345`
- `profile`: `baseline`
- `launch_file`: `figure8_payload_experiment.launch.py`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `reports/speed_sweep_validation_2026-07-22/omega_025/baseline_trial_02`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
