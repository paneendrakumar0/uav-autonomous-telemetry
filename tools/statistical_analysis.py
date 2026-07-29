#!/usr/bin/env python3
"""Small, deterministic statistical helpers for controller comparisons."""

from __future__ import annotations

import math
import random
import statistics
from collections.abc import Iterable
from typing import Any


def _finite_values(values: Iterable[float], label: str) -> list[float]:
    result = [float(value) for value in values]
    if len(result) < 2:
        raise ValueError(f"{label} requires at least two observations")
    if not all(math.isfinite(value) for value in result):
        raise ValueError(f"{label} contains a non-finite observation")
    return result


def _quantile(sorted_values: list[float], probability: float) -> float:
    if not sorted_values:
        raise ValueError("cannot calculate a quantile of an empty sample")
    position = (len(sorted_values) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return sorted_values[lower]
    fraction = position - lower
    return sorted_values[lower] + fraction * (sorted_values[upper] - sorted_values[lower])


def _resampled_mean(values: list[float], rng: random.Random) -> float:
    return statistics.fmean(rng.choice(values) for _ in values)


def hedges_g(baseline: Iterable[float], candidate: Iterable[float]) -> float | None:
    """Return bias-corrected standardized improvement; positive favors candidate."""
    baseline_values = _finite_values(baseline, "baseline")
    candidate_values = _finite_values(candidate, "candidate")
    baseline_variance = statistics.variance(baseline_values)
    candidate_variance = statistics.variance(candidate_values)
    degrees_of_freedom = len(baseline_values) + len(candidate_values) - 2
    pooled_variance = (
        (len(baseline_values) - 1) * baseline_variance
        + (len(candidate_values) - 1) * candidate_variance
    ) / degrees_of_freedom
    if pooled_variance <= 0.0:
        return None
    cohen_d = (
        statistics.fmean(baseline_values) - statistics.fmean(candidate_values)
    ) / math.sqrt(pooled_variance)
    correction = 1.0 - 3.0 / (4.0 * degrees_of_freedom - 1.0)
    return correction * cohen_d


def bootstrap_improvement(
    baseline: Iterable[float],
    candidate: Iterable[float],
    *,
    confidence_level: float = 0.95,
    resamples: int = 10_000,
    seed: int = 20_260_729,
) -> dict[str, Any]:
    """Compare independent samples for a lower-is-better metric.

    The absolute improvement is baseline minus candidate, so positive values
    favor the candidate controller.
    """
    baseline_values = _finite_values(baseline, "baseline")
    candidate_values = _finite_values(candidate, "candidate")
    if not 0.0 < confidence_level < 1.0:
        raise ValueError("confidence_level must be between 0 and 1")
    if resamples < 100:
        raise ValueError("resamples must be at least 100")

    baseline_mean = statistics.fmean(baseline_values)
    candidate_mean = statistics.fmean(candidate_values)
    absolute_improvement = baseline_mean - candidate_mean
    percent_improvement = (
        100.0 * absolute_improvement / baseline_mean
        if not math.isclose(baseline_mean, 0.0)
        else None
    )

    rng = random.Random(seed)
    absolute_samples = []
    percent_samples = []
    for _ in range(resamples):
        resampled_baseline = _resampled_mean(baseline_values, rng)
        resampled_candidate = _resampled_mean(candidate_values, rng)
        difference = resampled_baseline - resampled_candidate
        absolute_samples.append(difference)
        if not math.isclose(resampled_baseline, 0.0):
            percent_samples.append(100.0 * difference / resampled_baseline)

    absolute_samples.sort()
    percent_samples.sort()
    alpha = 1.0 - confidence_level
    lower_probability = alpha / 2.0
    upper_probability = 1.0 - lower_probability

    return {
        "baseline_n": len(baseline_values),
        "candidate_n": len(candidate_values),
        "baseline_mean": baseline_mean,
        "candidate_mean": candidate_mean,
        "absolute_improvement": absolute_improvement,
        "absolute_ci_low": _quantile(absolute_samples, lower_probability),
        "absolute_ci_high": _quantile(absolute_samples, upper_probability),
        "percent_improvement": percent_improvement,
        "percent_ci_low": (
            _quantile(percent_samples, lower_probability) if percent_samples else None
        ),
        "percent_ci_high": (
            _quantile(percent_samples, upper_probability) if percent_samples else None
        ),
        "hedges_g": hedges_g(baseline_values, candidate_values),
        "confidence_level": confidence_level,
        "bootstrap_resamples": resamples,
        "bootstrap_seed": seed,
    }
