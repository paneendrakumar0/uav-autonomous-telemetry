# Single Validation Run

**Created**: 2026-07-22T17:48:29
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
- `mean_3d_error_m`: `0.4450`
- `rms_3d_error_m`: `0.4755`
- `max_3d_error_m`: `0.6756`
- `mean_xy_error_m`: `0.4447`
- `mean_z_ned_m`: `-4.9990`
- `max_abs_position_m`: `5.3895`
- `mean_altitude_error_m`: `0.0010`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18542`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0012`
- `mean_lateral_swing_m`: `0.5645`
- `max_lateral_swing_m`: `0.7312`
- `mean_cable_angle_deg`: `34.6077`
- `max_cable_angle_deg`: `46.8629`
- `profile`: `baseline`
- `launch_file`: `figure8_payload_experiment.launch.py`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `reports/repeatability_validation_10x10_2026-07-22/baseline_trial_05`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
