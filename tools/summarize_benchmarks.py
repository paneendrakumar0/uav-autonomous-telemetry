#!/usr/bin/env python3
"""Summarize PX4/Gazebo trajectory and slung-payload benchmark CSVs."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class TrackingCase:
    name: str
    csv_path: Path
    steady_after_s: float
    profile: str


@dataclass(frozen=True)
class SwingCase:
    name: str
    csv_path: Path
    steady_after_s: float


def fmt(value: float, unit: str = "") -> str:
    if pd.isna(value):
        return "n/a"
    return f"{value:.3f}{unit}"


def tracking_metrics(case: TrackingCase) -> dict[str, str]:
    df = pd.read_csv(case.csv_path).dropna()
    steady = df[df["t_s"] >= case.steady_after_s]
    if steady.empty:
        steady = df

    xy_error = (steady["error_x"] ** 2 + steady["error_y"] ** 2) ** 0.5
    duration = float(df["t_s"].max() - df["t_s"].min()) if len(df) else float("nan")

    return {
        "case": case.name,
        "profile": case.profile,
        "samples": str(len(df)),
        "duration_s": fmt(duration),
        "window": f"t >= {case.steady_after_s:.0f} s",
        "mean_3d_error_m": fmt(float(steady["error_norm"].mean())),
        "rms_3d_error_m": fmt(float((steady["error_norm"] ** 2).mean() ** 0.5)),
        "max_3d_error_m": fmt(float(steady["error_norm"].max())),
        "mean_xy_error_m": fmt(float(xy_error.mean())),
        "mean_altitude_ned_m": fmt(float(steady["actual_z"].mean())),
        "final_altitude_ned_m": fmt(float(df["actual_z"].iloc[-1])),
    }


def swing_metrics(case: SwingCase) -> dict[str, str]:
    df = pd.read_csv(case.csv_path).dropna()
    steady = df[df["t_s"] >= case.steady_after_s]
    if steady.empty:
        steady = df

    return {
        "case": case.name,
        "samples": str(len(df)),
        "window": f"t >= {case.steady_after_s:.0f} s",
        "mean_lateral_swing_m": fmt(float(steady["lateral_swing_m"].mean())),
        "max_lateral_swing_m": fmt(float(steady["lateral_swing_m"].max())),
        "mean_cable_angle_deg": fmt(float(steady["cable_angle_deg"].mean())),
        "max_cable_angle_deg": fmt(float(steady["cable_angle_deg"].max())),
        "mean_cable_length_m": fmt(float(steady["cable_length_m"].mean())),
    }


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    labels = {
        "case": "Case",
        "profile": "Profile",
        "samples": "Samples",
        "duration_s": "Duration (s)",
        "window": "Steady Window",
        "mean_3d_error_m": "Mean 3D Error (m)",
        "rms_3d_error_m": "RMS 3D Error (m)",
        "max_3d_error_m": "Max 3D Error (m)",
        "mean_xy_error_m": "Mean XY Error (m)",
        "mean_altitude_ned_m": "Mean Z NED (m)",
        "final_altitude_ned_m": "Final Z NED (m)",
        "mean_lateral_swing_m": "Mean Lateral Swing (m)",
        "max_lateral_swing_m": "Max Lateral Swing (m)",
        "mean_cable_angle_deg": "Mean Cable Angle (deg)",
        "max_cable_angle_deg": "Max Cable Angle (deg)",
        "mean_cable_length_m": "Mean Cable Length (m)",
    }
    header = "| " + " | ".join(labels[col] for col in columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(row[col] for col in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    root = args.repo_root.resolve()
    tracking_cases = [
        TrackingCase(
            "No-payload Figure-8 tuned baseline",
            root / "reports/fig8_metrics_tuned_2026-06-04/figure8_tracking_metrics.csv",
            12.0,
            "Figure-8, position+velocity setpoints",
        ),
        TrackingCase(
            "Native ball-joint payload hover",
            root / "reports/payload_hover_native_ball_nocollision_2026-06-05/hover_tracking_metrics.csv",
            12.0,
            "Hover, physical payload attached",
        ),
        TrackingCase(
            "Native ball-joint payload Figure-8",
            root / "reports/payload_figure8_native_ball_2026-06-07/figure8_tracking_metrics.csv",
            25.0,
            "Figure-8, physical payload attached",
        ),
        TrackingCase(
            "Stage 4: Geometric omega=0.25",
            root / "reports/stage4_omega_025/figure8_tracking_metrics.csv",
            25.0,
            "Figure-8, geometric + smooth ramp",
        ),
        TrackingCase(
            "Stage 4: Geometric omega=0.20",
            root / "reports/stage4_omega_02/figure8_tracking_metrics.csv",
            25.0,
            "Figure-8, geometric + smooth ramp",
        ),
        TrackingCase(
            "Stage 4: Geometric omega=0.15",
            root / "reports/stage4_omega_015/figure8_tracking_metrics.csv",
            25.0,
            "Figure-8, geometric + smooth ramp",
        ),
    ]
    swing_cases = [
        SwingCase(
            "Native ball-joint payload hover",
            root / "reports/payload_hover_native_ball_nocollision_2026-06-05/payload_swing_metrics.csv",
            12.0,
        ),
        SwingCase(
            "Native ball-joint payload Figure-8",
            root / "reports/payload_figure8_native_ball_2026-06-07/payload_swing_metrics.csv",
            25.0,
        ),
        SwingCase(
            "Stage 4: Geometric omega=0.25",
            root / "reports/stage4_omega_025/payload_swing_metrics.csv",
            25.0,
        ),
        SwingCase(
            "Stage 4: Geometric omega=0.20",
            root / "reports/stage4_omega_02/payload_swing_metrics.csv",
            25.0,
        ),
        SwingCase(
            "Stage 4: Geometric omega=0.15",
            root / "reports/stage4_omega_015/payload_swing_metrics.csv",
            25.0,
        ),
    ]

    tracking_rows = [tracking_metrics(case) for case in tracking_cases]
    swing_rows = [swing_metrics(case) for case in swing_cases]

    text = f"""# Controller Benchmark Summary - 2026-06-08

This benchmark condenses the completed SITL runs into a single controller-performance view. The purpose is to establish a numerical baseline before moving from PX4 position/velocity offboard setpoints toward a geometric controller or payload-aware control law.

## Tracking Performance

{markdown_table(tracking_rows, [
    "case",
    "profile",
    "samples",
    "duration_s",
    "window",
    "mean_3d_error_m",
    "rms_3d_error_m",
    "max_3d_error_m",
    "mean_xy_error_m",
    "mean_altitude_ned_m",
    "final_altitude_ned_m",
])}

## Payload Swing Diagnostics

{markdown_table(swing_rows, [
    "case",
    "samples",
    "window",
    "mean_lateral_swing_m",
    "max_lateral_swing_m",
    "mean_cable_angle_deg",
    "max_cable_angle_deg",
    "mean_cable_length_m",
])}

## Interpretation

- The no-payload Figure-8 remains the clean reference case for evaluating controller changes.
- The native ball-joint payload model now climbs, hovers, and completes the requested 8-shaped circuit.
- The payload Figure-8 tracking error is close to the no-payload tuned baseline, which means the current PX4 offboard position/velocity interface is already a valid baseline for Professor Zavoli's requested test.
- The swing logger values are diagnostic rather than final physical truth, because they are reconstructed from Gazebo pose-sniffer packets and frame conventions. The next control milestone should include a tighter payload-state estimator before claiming swing-angle suppression.
"""

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
