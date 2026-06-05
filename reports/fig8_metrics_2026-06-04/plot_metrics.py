#!/usr/bin/env python3
import csv
from pathlib import Path

import matplotlib.pyplot as plt


BASE = Path(__file__).resolve().parent
CSV_PATH = BASE / "figure8_tracking_metrics.csv"


def load_rows():
    with CSV_PATH.open(newline="") as f:
        rows = [
            {key: float(value) for key, value in row.items()}
            for row in csv.DictReader(f)
        ]

    if not rows:
        raise SystemExit(f"No rows in {CSV_PATH}")

    return rows


def metric_summary(rows, start_time=0.0):
    selected = [row for row in rows if row["t_s"] >= start_time]
    if not selected:
        selected = rows
    errors = [row["error_norm"] for row in selected]
    mean_error = sum(errors) / len(errors)
    rms_error = (sum(error * error for error in errors) / len(errors)) ** 0.5
    return {
        "samples": len(selected),
        "duration_s": selected[-1]["t_s"] - selected[0]["t_s"],
        "mean_error": mean_error,
        "rms_error": rms_error,
        "max_error": max(errors),
    }


def plot_xy(rows):
    fig, ax = plt.subplots(figsize=(7, 6), dpi=150)
    ax.plot([row["reference_x"] for row in rows], [row["reference_y"] for row in rows], label="reference", linewidth=2)
    ax.plot([row["actual_x"] for row in rows], [row["actual_y"] for row in rows], label="actual", linewidth=2, alpha=0.85)
    ax.set_title("Figure-8 Actual vs Reference: X-Y")
    ax.set_xlabel("x North [m]")
    ax.set_ylabel("y East [m]")
    ax.axis("equal")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(BASE / "actual_vs_reference_xy.png")
    plt.close(fig)


def plot_xyz_time(rows):
    fig, axes = plt.subplots(3, 1, figsize=(9, 8), dpi=150, sharex=True)
    for ax, axis in zip(axes, ["x", "y", "z"]):
        ax.plot([row["t_s"] for row in rows], [row[f"reference_{axis}"] for row in rows], label=f"{axis} reference")
        ax.plot([row["t_s"] for row in rows], [row[f"actual_{axis}"] for row in rows], label=f"{axis} actual", alpha=0.85)
        ax.set_ylabel(f"{axis} [m]")
        ax.grid(True, alpha=0.3)
        ax.legend(loc="upper right")
    axes[-1].set_xlabel("time [s]")
    fig.suptitle("Figure-8 Actual vs Reference: Position")
    fig.tight_layout()
    fig.savefig(BASE / "actual_vs_reference_xyz_time.png")
    plt.close(fig)


def plot_error(rows):
    fig, ax = plt.subplots(figsize=(9, 4.8), dpi=150)
    ax.plot([row["t_s"] for row in rows], [row["error_norm"] for row in rows], linewidth=1.5)
    ax.axvline(12.0, color="black", linestyle="--", linewidth=1, label="post-takeoff window")
    ax.set_title("Figure-8 Tracking Error")
    ax.set_xlabel("time [s]")
    ax.set_ylabel("position error norm [m]")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(BASE / "tracking_error_time.png")
    plt.close(fig)


def write_report(rows):
    full = metric_summary(rows)
    steady = metric_summary(rows, start_time=12.0)
    with (BASE / "METRICS.md").open("w") as f:
        f.write("# Figure-8 Tracking Metrics\n\n")
        f.write("## Full Run\n\n")
        f.write(f"- Samples: {full['samples']}\n")
        f.write(f"- Duration: {full['duration_s']:.2f} s\n")
        f.write(f"- Mean position error: {full['mean_error']:.3f} m\n")
        f.write(f"- RMS position error: {full['rms_error']:.3f} m\n")
        f.write(f"- Max position error: {full['max_error']:.3f} m\n\n")
        f.write("## Post-Takeoff Window, t >= 12 s\n\n")
        f.write(f"- Samples: {steady['samples']}\n")
        f.write(f"- Duration: {steady['duration_s']:.2f} s\n")
        f.write(f"- Mean position error: {steady['mean_error']:.3f} m\n")
        f.write(f"- RMS position error: {steady['rms_error']:.3f} m\n")
        f.write(f"- Max position error: {steady['max_error']:.3f} m\n\n")
        f.write("Plots:\n\n")
        f.write("- `actual_vs_reference_xy.png`\n")
        f.write("- `actual_vs_reference_xyz_time.png`\n")
        f.write("- `tracking_error_time.png`\n")

    print(f"full: samples={full['samples']} mean={full['mean_error']:.3f} rms={full['rms_error']:.3f} max={full['max_error']:.3f}")
    print(f"steady: samples={steady['samples']} mean={steady['mean_error']:.3f} rms={steady['rms_error']:.3f} max={steady['max_error']:.3f}")


def main():
    rows = load_rows()
    plot_xy(rows)
    plot_xyz_time(rows)
    plot_error(rows)
    write_report(rows)


if __name__ == "__main__":
    main()
