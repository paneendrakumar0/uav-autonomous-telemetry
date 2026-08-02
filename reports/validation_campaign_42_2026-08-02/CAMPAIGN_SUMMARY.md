# 42-Run UAV Slung-Payload Validation Campaign

**Campaign date:** 2026-08-02  
**Repository branch:** `phase/42-run-validation-campaign-2026-08-02`  
**Pinned campaign code:** `a3f0aab7ac14c9ce43ad033925310ac102dfb63a`  
**PX4:** v1.14.4 (`1555f2bd2229544c43966ab5f94879c41d8e1e01`)  
**Environment:** Ubuntu 22.04, ROS 2 Humble, Gazebo Classic 11, Micro XRCE-DDS Agent 2.4.3

## Outcome

The full campaign completed successfully:

- Official flights: **42/42 completed**
- Valid tracking telemetry: **42/42**
- Valid payload-swing telemetry: **42/42**
- Nominal repeatability: 5 baseline + 5 geometric
- Screening matrix: 10 wind + 6 altitude + 6 speed + 6 payload-mass + 4 gust/updraft
- Deterministic randomized execution order retained in both phase folders
- Raw tracking and payload telemetry retained in the isolated validation environment
- Original PX4 payload SDF restored byte-for-byte after the randomized matrix
- Post-campaign Python tests: **12/12 passed**

Aborted infrastructure-diagnostic attempts were preserved separately and are not included in the 42 official flights.

## Main Findings

### Nominal repeatability (5 trials per controller)

Compared with the PX4 position/velocity baseline, the geometric controller:

- Increased mean 3D tracking error by **18.16%**
- Increased RMS 3D tracking error by **25.50%**
- Reduced mean lateral payload swing by **8.53%**
- Reduced mean cable angle by **9.32%**

The nominal evidence therefore shows a controller tradeoff, not a general performance improvement.

### Remaining 16 paired screening conditions

- Geometric control reduced mean cable angle in **16/16** pairs.
- Cable-angle improvement ranged from **6.86% to 15.46%**.
- Geometric control improved mean 3D tracking error in only **3/16** pairs:
  - `omega_020`: **10.38%**
  - `altitude_3m`: **17.23%**
  - `omega_030`: **17.53%**
- Geometric control worsened mean 3D tracking in **13/16** pairs.

The largest weakness is steady crosswind rejection:

| Crosswind | Baseline mean 3D error | Geometric mean 3D error | Geometric change |
| --- | ---: | ---: | ---: |
| 2.5 m/s | 0.5433 m | 0.7363 m | 35.52% worse |
| 5.0 m/s | 0.4826 m | 1.3516 m | 180.04% worse |
| 7.5 m/s | 0.5583 m | 1.9856 m | 255.62% worse |
| 10.0 m/s | 0.5994 m | 2.6432 m | 341.01% worse |

The geometric controller consistently suppresses payload angle better, but its present attitude/thrust formulation lacks adequate steady-disturbance rejection for trajectory tracking.

## Scientific Interpretation

This is now a credible, reproducible simulation screening project rather than a demonstration-only project. It has pinned software versions, deterministic run ordering, raw telemetry, automated validity gates, paired conditions, uncertainty estimates for the nominal repeatability block, and explicit retention of negative results.

It is not yet a research-lab-complete or cutting-edge result. The screening families contain only one run per controller/condition, all evidence is from one SITL stack, and there is no hardware validation, estimator-noise study, sensor/actuator uncertainty campaign, controller ablation, or comparison against stronger disturbance-rejection baselines.

## Recommended Next Research Phase

1. Add integral or disturbance-observer action to the geometric controller and target the crosswind tracking failure.
2. Freeze the revised controller before evaluation; do not tune against the final test set.
3. Repeat the key wind conditions with at least 5 independent trials per controller and randomized order.
4. Add Monte Carlo sensor noise, parameter uncertainty, latency, and actuator saturation.
5. Compare against PX4 baseline plus at least one modern robust/nonlinear controller.
6. Progress to hardware-in-the-loop and then restrained flight testing with safety review.

## Artifacts

- `01_nominal_repeatability/REPEATABILITY_SUMMARY.md`
- `01_nominal_repeatability/repeatability_trial_metrics.csv`
- `01_nominal_repeatability/repeatability_statistical_comparison.csv`
- `02_remaining_matrix/REMAINING_CAMPAIGN_SUMMARY.md`
- `02_remaining_matrix/remaining_run_metrics.csv`
- `02_remaining_matrix/remaining_controller_comparison.csv`
- Per-run raw telemetry, plots, summaries, and manifests in the isolated Ubuntu 22.04 validation workspace
