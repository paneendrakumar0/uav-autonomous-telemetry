# Single Validation Run

**Created**: 2026-08-02T10:45:57
**Profile**: `hover`
**Launch File**: `payload_hover_experiment.launch.py`
**World**: `none`
**Flight Duration**: `35.0 s`
**Omega**: `0.25`
**Hover Thrust**: `0.72`

## Result

- Tracking valid: `True`
- Tracking reason: valid tracking telemetry
- Payload swing reason: valid payload swing telemetry

## Metrics

- `samples`: `3995`
- `duration_s`: `33.9442`
- `mean_3d_error_m`: `0.0790`
- `rms_3d_error_m`: `0.0803`
- `max_3d_error_m`: `0.1083`
- `mean_xy_error_m`: `0.0587`
- `mean_z_ned_m`: `-5.0526`
- `max_abs_position_m`: `5.0778`
- `mean_altitude_error_m`: `0.0526`
- `swing_valid`: `True`
- `swing_reason`: `valid payload swing telemetry`
- `swing_samples`: `7944`
- `pose_source`: `gazebo_link_pair`
- `mean_cable_length_m`: `1.0000`
- `mean_lateral_swing_m`: `0.0112`
- `max_lateral_swing_m`: `0.0187`
- `mean_cable_angle_deg`: `0.6400`
- `max_cable_angle_deg`: `1.0736`
- `profile`: `hover`
- `launch_file`: `payload_hover_experiment.launch.py`
- `world`: `none`
- `tracking_valid`: `True`
- `tracking_reason`: `valid tracking telemetry`
- `output_dir`: `reports/readiness_smoke_2026-08-02`

## Expected Artifacts

The runner writes the manifest. Generate the plots with `tools/plot_validation_run.py <run_dir>`:

- `validation_xy_tracking.png`
- `validation_3d_tracking.png`
- `validation_xyz_vs_time.png`
- `validation_error_swing.png`
- `experiment_manifest.json`
