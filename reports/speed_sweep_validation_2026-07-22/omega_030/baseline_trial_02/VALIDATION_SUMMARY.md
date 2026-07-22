# Single Validation Run

**Created**: 2026-07-22T19:01:45
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

- `samples`: `3708`
- `duration_s`: `74.1400`
- `mean_3d_error_m`: `0.6791`
- `rms_3d_error_m`: `0.7223`
- `max_3d_error_m`: `1.0510`
- `mean_xy_error_m`: `0.6789`
- `mean_z_ned_m`: `-4.9965`
- `max_abs_position_m`: `5.7033`
- `mean_altitude_error_m`: `0.0035`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18540`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0016`
- `mean_lateral_swing_m`: `0.6566`
- `max_lateral_swing_m`: `0.8051`
- `mean_cable_angle_deg`: `41.3939`
- `max_cable_angle_deg`: `53.4328`
- `profile`: `baseline`
- `launch_file`: `figure8_payload_experiment.launch.py`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `reports/speed_sweep_validation_2026-07-22/omega_030/baseline_trial_02`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
