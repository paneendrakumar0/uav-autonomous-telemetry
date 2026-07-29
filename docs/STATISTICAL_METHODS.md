# Statistical Methods

## Scope

Uncertainty estimates are generated only for campaigns with at least two
observations per controller. Single-run payload and wind screenings remain
screening evidence and do not receive inferential statistics.

## Controller comparison

For each lower-is-better metric, the reported absolute improvement is:

```text
mean(PX4 baseline) - mean(geometric controller)
```

A positive value therefore favors the geometric controller. Percent
improvement uses the PX4 baseline mean as the denominator.

The initial metrics are:

- mean 3D tracking error;
- RMS 3D tracking error;
- mean lateral payload swing;
- mean cable angle.

## Confidence intervals

The analysis uses independent-sample percentile bootstrap intervals. Baseline
and geometric trials are resampled independently with replacement. The default
configuration is:

- confidence level: `0.95`;
- resamples: `10,000`;
- root seed: `20260729`.

Seeds are recorded in the experiment manifest. Metric and speed comparisons
derive deterministic child seeds from the root seed, making regenerated tables
byte-for-byte repeatable for the same input data and Python implementation.

## Standardized effect

Hedges' `g` reports the bias-corrected standardized mean difference. Its sign is
oriented so that a positive value favors the geometric controller. It is
reported as `n/a` when both samples have zero pooled variance.

Near-deterministic SITL trials can produce very small pooled variance and
therefore extremely large standardized effects. Such values describe separation
relative to simulator repeatability; they are not estimates of real-world
effect magnitude.

## Interpretation limits

A bootstrap confidence interval quantifies sampling uncertainty in the
available trials; it does not correct a deterministic or poorly randomized
experiment. The current SITL trials may share common simulator conditions and
must not be treated as independent real-world flights.

Publication claims still require:

- randomized initial payload states, wind/noise realizations, and run order;
- declared seeds;
- a justified sample count or power analysis;
- inspection of distribution shape and outliers;
- correction or explicit scoping when many hypotheses are tested;
- hardware or HIL replication for real-world claims.
