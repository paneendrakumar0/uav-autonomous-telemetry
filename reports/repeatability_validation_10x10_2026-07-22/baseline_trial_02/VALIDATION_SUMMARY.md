# Single Validation Run

**Created**: 2026-07-22T17:43:01
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
- `duration_s`: `74.1638`
- `mean_3d_error_m`: `0.4429`
- `rms_3d_error_m`: `0.4731`
- `max_3d_error_m`: `0.6715`
- `mean_xy_error_m`: `0.4425`
- `mean_z_ned_m`: `-4.9987`
- `max_abs_position_m`: `5.3879`
- `mean_altitude_error_m`: `0.0013`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `18545`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0012`
- `mean_lateral_swing_m`: `0.5638`
- `max_lateral_swing_m`: `0.7318`
- `mean_cable_angle_deg`: `34.5612`
- `max_cable_angle_deg`: `46.9139`
- `profile`: `baseline`
- `launch_file`: `figure8_payload_experiment.launch.py`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `reports/repeatability_validation_10x10_2026-07-22/baseline_trial_02`

## Expected Plot Artifacts

Generate these with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
