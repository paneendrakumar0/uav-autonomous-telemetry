# Wind Feed-Forward and Payload-Swing Feedback V1

## Research Question

Can a bounded acceleration-disturbance observer recover crosswind tracking while explicit cable-state feedback preserves or improves payload-swing suppression?

This phase changes controller structure rather than retuning the rejected integral candidate. Integral gains remain zero by default.

## Controller Structure

The geometric acceleration command is extended by two independently switchable terms:

1. **Disturbance feed-forward:** low-pass the difference between measured horizontal acceleration and the previously applied acceleration command, bound the estimate, and subtract a gain-scaled estimate from the next command.
2. **Payload-swing feedback:** derive the normalized cable direction and filtered direction rate from the calibrated Gazebo UAV/payload link pair, transform Gazebo ENU vectors to PX4 local NED, then command a bounded horizontal acceleration toward the displaced payload with rate damping.

Both terms have zero default gain. A stale payload-state timeout and the existing tilt/thrust saturation limits remain active. Estimated disturbance and payload correction are retained in raw telemetry.

## Development Set

- Vehicle and payload: `iris_depth_payload`, 0.05 kg payload, 1.0 m cable
- Figure-8: amplitude 5 m, angular rate 0.25 rad/s, altitude 5 m
- Constant Y-crosswinds: 0, 5, and 10 m/s
- Development runs are screening data and must not enter the frozen evaluation dataset.
- Tune observer-only, swing-only, and then combined candidates.
- Reject a candidate immediately for invalid telemetry, mean altitude error above 1.5 m, excessive position, persistent saturation, or stale payload state.

## Freeze Rule

Freeze at most one combined candidate. Relative to the PX4 baseline, the candidate should:

- avoid a meaningful tracking regression at 0 m/s;
- improve mean 3D tracking error at 5 and 10 m/s;
- retain a positive payload cable-angle benefit at every wind;
- keep the 95% interval and all negative results in the final report.

## Official Evaluation

After gains are frozen, run 30 randomized flights: baseline and candidate at 0, 5, and 10 m/s, five trials per controller/wind cell. Use a new fixed run-order seed, retain raw telemetry, generate bootstrap confidence intervals, and prohibit gain changes after the first official flight starts.
