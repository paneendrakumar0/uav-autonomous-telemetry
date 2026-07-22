# Research Product Roadmap

This document defines the path from the current PX4/ROS 2/Gazebo slung-payload validation prototype to a serious academic and industrial research product. The target standard is not a demonstration video; it is a defensible experimental platform with reproducible runs, explicit validation gates, publishable controller comparisons, and clear evidence for every claim.

## Current Baseline

Stable baseline as of `2026-07-22`:

- PX4 SITL + Gazebo Classic `iris_depth_payload` vehicle runs with a native ball-joint slung payload.
- ROS 2 offboard control and MicroXRCEAgent bridge are operational.
- Baseline PX4 position/velocity Figure-8 controller is validated.
- Tuned geometric attitude/thrust Figure-8 controller is validated.
- Calibrated same-frame Gazebo link-pair payload swing logger is operational.
- Controlled single-run validation harness is available.
- Controlled repeatability harness is available.
- Latest clean repeatability set: `5` baseline trials + `5` geometric trials.

Latest controlled `5+5` result:

| Metric | PX4 Baseline | Tuned Geometric | Improvement |
| --- | ---: | ---: | ---: |
| Mean 3D tracking error | `0.4452 m` | `0.3466 m` | `22.1%` |
| RMS 3D tracking error | `0.4752 m` | `0.3662 m` | `22.9%` |
| Mean lateral payload swing | `0.5641 m` | `0.5127 m` | `9.1%` |
| Mean cable angle | `34.5806 deg` | `31.0270 deg` | `10.3%` |

Evidence:

- `reports/repeatability_validation_5x5_2026-07-21/REPEATABILITY_SUMMARY.md`
- `reports/repeatability_validation_2026-07-21/REPEATABILITY_SUMMARY.md`
- `reports/single_validation_2026-07-21_controller_comparison/CONTROLLED_BASELINE_VS_GEOMETRIC.md`
- `reports/geometric_altitude_tuning_2026-06-12/GEOMETRIC_ALTITUDE_TUNING_REPORT.md`

## Research Objective

Develop and validate an autonomous UAV slung-payload simulation and control framework that can support publishable comparisons between conventional PX4 offboard control and geometric/payload-aware control methods for aggressive but controlled waypoint and Figure-8 trajectories.

The research contribution should be framed around:

- reproducible PX4/ROS 2/Gazebo slung-payload SITL environment;
- calibrated payload swing telemetry;
- controlled Figure-8 trajectory benchmark;
- repeatable comparison between baseline PX4 offboard control and geometric attitude/thrust control;
- progressive extension toward payload-aware control and trajectory optimization.

## Non-Negotiable Engineering Standards

Every future phase must satisfy these rules before commit and push:

1. Start from a clean Git state.
2. Use scripted launch and validation, not manual terminal state.
3. Explicitly start and stop `MicroXRCEAgent`, PX4 SITL, Gazebo, and ROS 2.
4. Validate PX4 local position magnitude.
5. Validate mean altitude reaches the commanded Figure-8 altitude.
6. Validate payload telemetry source is `gazebo_link_pair`.
7. Validate cable length remains physically close to the modeled cable length.
8. Remove runtime logs before commit.
9. Store summaries, plots, and aggregate CSVs in Git.
10. Avoid committing large raw telemetry unless a specific phase requires it.
11. Commit and push each completed phase before starting the next.

## Phase Roadmap

### Phase 1: Documentation Alignment

Goal: make the repository readable as a serious research artifact.

Tasks:

- Update `README.md` to show the current July controlled-validation state.
- Add a concise current-results table.
- Link the latest repeatability reports.
- Separate historical debugging from final validated results.

Exit criteria:

- README does not imply old failed payload stages are the current state.
- Latest results are visible in the first screen.
- All links resolve locally.

Deliverable:

- Commit: README/status refresh.

### Phase 2: Repeatability Scale-Up, `10+10`

Goal: confirm the `5+5` result holds over a larger sample.

Tasks:

- Run `10` PX4 baseline trials.
- Run `10` tuned geometric trials.
- Use the strengthened validation gates:
  - local-position bound;
  - mean altitude near `-5 m`;
  - valid payload swing telemetry;
  - cable length sanity.
- Store aggregate CSVs, summaries, and plots.

Exit criteria:

- At least `20/20` valid trials, or a documented failure report explaining any invalid trial.
- Aggregate mean and standard deviation reported.
- Controller improvement remains positive for tracking and swing metrics.

Deliverable:

- `reports/repeatability_validation_10x10_<date>/REPEATABILITY_SUMMARY.md`

### Phase 3: Figure-8 Speed Sweep

Goal: characterize the tracking/swing tradeoff as trajectory aggressiveness changes.

Test rates:

- `omega = 0.15 rad/s`
- `omega = 0.20 rad/s`
- `omega = 0.25 rad/s`
- optional: `omega = 0.30 rad/s` only if stability remains acceptable.

Tasks:

- Run baseline and geometric controller for each rate.
- Use at least `3` valid trials per controller per rate.
- Report tracking error, RMS error, lateral swing, cable angle, and altitude bias.

Exit criteria:

- A clear performance envelope showing where geometric control helps most.
- Identification of safe and unsafe/aggressive regimes.

Deliverable:

- Speed-sweep report with plots and controller tradeoff table.

### Phase 4: Payload Parameter Sweep

Goal: test robustness across payload mass and cable length.

Parameters:

- payload mass: light, nominal, heavy;
- cable length: short, nominal, long.

Tasks:

- Version payload SDF parameters cleanly.
- Run controlled Figure-8 trials for each parameter set.
- Evaluate tracking degradation and swing growth.

Exit criteria:

- Controller comparison remains interpretable across payload conditions.
- Any unstable payload regime is documented with evidence.

Deliverable:

- Payload robustness report.

### Phase 5: Payload-Aware Controller Design

Goal: move beyond geometric UAV-only control toward a publishable control contribution.

Candidate directions:

- cable-angle feedback damping;
- payload-position feedback through estimated relative state;
- trajectory shaping with swing suppression;
- differential-flatness or geometric controller extension for suspended loads.

Tasks:

- Implement one payload-aware controller variant.
- Compare against:
  - PX4 position/velocity baseline;
  - tuned geometric attitude/thrust controller.
- Use identical Figure-8 and repeatability validation.

Exit criteria:

- Payload-aware controller reduces swing without unacceptable tracking loss.
- Results are statistically repeatable.

Deliverable:

- Controller contribution report and code.

### Phase 6: Trajectory Optimization

Goal: generate trajectories that explicitly trade off speed, tracking accuracy, and payload swing.

Tasks:

- Define trajectory cost:
  - tracking error;
  - cable angle;
  - swing velocity or lateral displacement;
  - control smoothness;
  - mission duration.
- Generate reference trajectories offline.
- Execute them in PX4 SITL through ROS 2.

Exit criteria:

- Optimized references reduce swing compared with naive Figure-8 at similar traversal time.

Deliverable:

- Trajectory optimization report and generated trajectory artifacts.

### Phase 7: Perception Integration

Goal: reconnect the depth-camera pipeline to autonomous navigation.

Tasks:

- Validate camera topics and point cloud.
- Add occupancy mapping baseline.
- Create obstacle-aware waypoint or corridor-following scenario.
- Keep payload swing metrics active during perception-driven flight.

Exit criteria:

- Perception stack affects navigation decisions.
- Payload metrics remain logged and valid.

Deliverable:

- Autonomous perception + payload flight report.

### Phase 8: Industrial-Grade Reproducibility

Goal: make the project usable by another researcher or lab.

Tasks:

- Add one-command environment check.
- Add scripted PX4 integration sync.
- Add run manifests recording:
  - Git commit;
  - PX4 commit/state;
  - controller parameters;
  - trajectory parameters;
  - validation thresholds.
- Add CI-style offline checks for scripts and report generation.

Exit criteria:

- A new machine can reproduce at least one validation run from instructions.
- Every report identifies the code and parameters used.

Deliverable:

- Reproducibility package.

### Phase 9: Publication Package

Goal: prepare material suitable for a workshop/conference submission.

Tasks:

- Write paper-style report:
  - abstract;
  - introduction;
  - related work;
  - system architecture;
  - controller formulation;
  - experimental protocol;
  - results;
  - limitations;
  - conclusion.
- Generate final figures at publication quality.
- Create professor-ready slide deck.
- Prepare repository release tag.

Exit criteria:

- Claims are supported by repeatability data.
- Figures are readable without local context.
- Limitations are explicit and defensible.

Deliverable:

- Paper draft, figures, and tagged code release.

## Immediate Next Stage

The next technical stage should be **Phase 1: Documentation Alignment**, because the experimental evidence is now stronger than the repository front page. The project should not continue accumulating experiments while the README still emphasizes old debugging failures.

After that, proceed to **Phase 2: `10+10` repeatability scale-up**.

## Current Open Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Gazebo Classic aging/deprecation | Long-term reproducibility risk | Keep Classic stable now; plan controlled Gazebo Sim migration later |
| Raw telemetry size | GitHub push failures and repository bloat | Store aggregate CSVs and plots; keep raw CSVs local or release-asset only |
| Single trajectory type | Narrow claim scope | Add speed sweep and waypoint/circuit scenarios |
| Controller not yet payload-aware | Limited novelty | Add payload-state feedback or trajectory shaping phase |
| Simulation-only validation | Industrial realism limit | Improve disturbance, payload parameter, and sensor/noise studies |
| Manual PX4 integration state | Reproducibility risk | Add sync/check script and run manifests |

## Definition of a Publishable Result

A result is publishable only if all of the following are true:

- same experiment can be rerun from scripts;
- all invalid trials are reported, not hidden;
- controller comparison uses matched trajectory parameters;
- payload measurements come from a calibrated same-frame source;
- at least one repeatability set supports each key claim;
- plots and tables can be read independently of terminal logs;
- limitations are stated explicitly.

