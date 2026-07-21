#!/usr/bin/env python3
import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def values(series):
    return series.to_numpy()


def load_csv(path):
    if not path.exists():
        raise SystemExit(f"Missing required CSV: {path}")
    df = pd.read_csv(path)
    if df.empty:
        raise SystemExit(f"CSV has no data: {path}")
    return df


def plot_xy(tracking, out_dir):
    fig, ax = plt.subplots(figsize=(7, 6), dpi=150)
    ax.plot(values(tracking["reference_x"]), values(tracking["reference_y"]), label="reference", linewidth=2.0)
    ax.plot(values(tracking["actual_x"]), values(tracking["actual_y"]), label="actual", linewidth=1.8, alpha=0.85)
    ax.set_title("Figure-8 XY Tracking")
    ax.set_xlabel("x North [m]")
    ax.set_ylabel("y East [m]")
    ax.axis("equal")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_dir / "validation_xy_tracking.png")
    plt.close(fig)


def plot_3d(tracking, out_dir):
    fig = plt.figure(figsize=(8, 6), dpi=150)
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(
        values(tracking["reference_x"]),
        values(tracking["reference_y"]),
        values(-tracking["reference_z"]),
        label="reference",
        linewidth=2.0,
    )
    ax.plot(
        values(tracking["actual_x"]),
        values(tracking["actual_y"]),
        values(-tracking["actual_z"]),
        label="actual",
        linewidth=1.8,
        alpha=0.85,
    )
    ax.set_title("Figure-8 3D Tracking")
    ax.set_xlabel("x North [m]")
    ax.set_ylabel("y East [m]")
    ax.set_zlabel("altitude [m]")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_dir / "validation_3d_tracking.png")
    plt.close(fig)


def plot_xyz_time(tracking, out_dir):
    fig, axes = plt.subplots(3, 1, figsize=(9, 8), dpi=150, sharex=True)
    for ax, axis in zip(axes, ["x", "y", "z"]):
        ax.plot(values(tracking["t_s"]), values(tracking[f"reference_{axis}"]), label=f"{axis} reference")
        ax.plot(values(tracking["t_s"]), values(tracking[f"actual_{axis}"]), label=f"{axis} actual", alpha=0.85)
        ax.set_ylabel(f"{axis} [m]")
        ax.grid(True, alpha=0.3)
        ax.legend(loc="upper right")
    axes[-1].set_xlabel("time [s]")
    fig.suptitle("Figure-8 XYZ Coordinates vs Time")
    fig.tight_layout()
    fig.savefig(out_dir / "validation_xyz_vs_time.png")
    plt.close(fig)


def plot_error_and_swing(tracking, swing, out_dir):
    fig, axes = plt.subplots(3, 1, figsize=(9, 8), dpi=150, sharex=False)
    axes[0].plot(values(tracking["t_s"]), values(tracking["error_norm"]), linewidth=1.5)
    axes[0].axvline(25.0, color="black", linestyle="--", linewidth=1.0, label="steady window")
    axes[0].set_ylabel("3D error [m]")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend(loc="upper right")

    axes[1].plot(values(swing["t_s"]), values(swing["lateral_swing_m"]), linewidth=1.5, color="tab:orange")
    axes[1].axvline(25.0, color="black", linestyle="--", linewidth=1.0)
    axes[1].set_ylabel("lateral swing [m]")
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(values(swing["t_s"]), values(swing["cable_angle_deg"]), linewidth=1.5, color="tab:green")
    axes[2].axvline(25.0, color="black", linestyle="--", linewidth=1.0)
    axes[2].set_xlabel("time [s]")
    axes[2].set_ylabel("cable angle [deg]")
    axes[2].grid(True, alpha=0.3)

    fig.suptitle("Tracking Error and Payload Swing Diagnostics")
    fig.tight_layout()
    fig.savefig(out_dir / "validation_error_swing.png")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Generate plots for a single validation run folder.")
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()

    run_dir = args.run_dir.expanduser()
    tracking = load_csv(run_dir / "tracking_metrics.csv")
    swing = load_csv(run_dir / "payload_swing_metrics.csv")

    plot_xy(tracking, run_dir)
    plot_3d(tracking, run_dir)
    plot_xyz_time(tracking, run_dir)
    plot_error_and_swing(tracking, swing, run_dir)
    print(f"Plots written to {run_dir}")


if __name__ == "__main__":
    main()
