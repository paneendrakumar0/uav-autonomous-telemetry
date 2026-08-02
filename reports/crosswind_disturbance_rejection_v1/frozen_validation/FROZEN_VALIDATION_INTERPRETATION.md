# Frozen Crosswind Candidate: Decision Record

## Decision

The frozen `ki_xy=0.35`, `kd_xy=1.3`, 35-degree-tilt candidate is **not accepted as a replacement controller**.

All 30 planned flights were completed with valid tracking and payload-swing telemetry. The candidate reduced payload cable angle at every tested wind speed, but it did not satisfy the predeclared rule that tracking must also improve.

## Primary Results

| Crosswind | Baseline mean 3D error | Candidate mean 3D error | Tracking result | Cable-angle improvement (95% bootstrap CI) |
| --- | ---: | ---: | --- | ---: |
| 0 m/s | 0.4388 m | 0.4895 m | 11.56% worse; inconclusive CI | 4.65% (3.82%, 5.45%) |
| 5 m/s | 0.4512 m | 0.5025 m | 11.36% worse; inconclusive CI | 5.17% (4.26%, 6.10%) |
| 10 m/s | 0.4762 m | 1.4345 m | 201.22% worse; CI excludes zero | 7.22% (6.75%, 7.74%) |

Positive cable-angle improvement means less payload swing. Tracking confidence intervals and all secondary metrics are retained in `crosswind_statistical_comparison.csv`.

## Interpretation

The integral term trades vehicle path accuracy for payload-angle reduction and becomes unsuitable at 10 m/s. The result supports the disturbance-rejection mechanism as a useful research prototype, but rejects this gain structure as a deployable controller. More gain-only tuning against these evaluation flights would compromise the frozen-test protocol and is not justified.

The next research phase should change the controller structure: add measured or estimated wind feed-forward and explicit payload-swing state feedback, then tune only on a separate development set. A new frozen branch should be evaluated on untouched randomized trials before any replacement is merged.

## Execution Note

After 20 valid flights, the WSL simulation service produced an operating-system I/O failure before flight 21 acquired telemetry. The service was restarted, the 20 valid summaries were reused through the runner's `--resume` mode, and flight 21 was rerun from the beginning. No partial flight entered the dataset, and the seeded 30-flight order was preserved.
