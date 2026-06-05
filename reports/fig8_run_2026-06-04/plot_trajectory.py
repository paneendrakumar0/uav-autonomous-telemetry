#!/usr/bin/env python3
import csv
from pathlib import Path

import matplotlib.pyplot as plt


BASE = Path(__file__).resolve().parent
CSV_PATH = BASE / "local_position_trace.csv"


def load_samples():
    samples = []
    with CSV_PATH.open(newline="") as f:
        for row in csv.reader(f):
            if len(row) < 18:
                continue
            try:
                timestamp = float(row[0]) * 1e-6
                samples.append(
                    {
                        "t": timestamp,
                        "x": float(row[6]),
                        "y": float(row[7]),
                        "z": float(row[8]),
                        "vx": float(row[14]),
                        "vy": float(row[15]),
                        "vz": float(row[16]),
                    }
                )
            except ValueError:
                continue

    if not samples:
        raise SystemExit(f"No trajectory samples parsed from {CSV_PATH}")

    t0 = samples[0]["t"]
    for sample in samples:
        sample["t"] -= t0

    return samples


def save_xy(samples):
    fig, ax = plt.subplots(figsize=(7, 6), dpi=150)
    ax.plot([s["x"] for s in samples], [s["y"] for s in samples], linewidth=2)
    ax.scatter(samples[0]["x"], samples[0]["y"], color="green", label="start", s=28)
    ax.scatter(samples[-1]["x"], samples[-1]["y"], color="red", label="end", s=28)
    ax.set_title("Figure-8 Flight Trace: X-Y")
    ax.set_xlabel("x North [m]")
    ax.set_ylabel("y East [m]")
    ax.axis("equal")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(BASE / "figure8_xy.png")
    plt.close(fig)


def save_xyz_time(samples):
    fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
    t = [s["t"] for s in samples]
    ax.plot(t, [s["x"] for s in samples], label="x")
    ax.plot(t, [s["y"] for s in samples], label="y")
    ax.plot(t, [s["z"] for s in samples], label="z")
    ax.set_title("Figure-8 Local Position vs Time")
    ax.set_xlabel("time [s]")
    ax.set_ylabel("position [m]")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(BASE / "figure8_xyz_vs_time.png")
    plt.close(fig)


def save_3d(samples):
    fig = plt.figure(figsize=(7, 6), dpi=150)
    ax = fig.add_subplot(111, projection="3d")
    ax.plot([s["x"] for s in samples], [s["y"] for s in samples], [-s["z"] for s in samples], linewidth=2)
    ax.set_title("Figure-8 Flight Trace: 3D")
    ax.set_xlabel("x North [m]")
    ax.set_ylabel("y East [m]")
    ax.set_zlabel("altitude [m]")
    fig.tight_layout()
    fig.savefig(BASE / "figure8_3d.png")
    plt.close(fig)


def main():
    samples = load_samples()
    save_xy(samples)
    save_xyz_time(samples)
    save_3d(samples)

    duration = samples[-1]["t"] - samples[0]["t"]
    print(f"samples={len(samples)} duration_s={duration:.2f}")
    print(f"x_range=({min(s['x'] for s in samples):.2f}, {max(s['x'] for s in samples):.2f})")
    print(f"y_range=({min(s['y'] for s in samples):.2f}, {max(s['y'] for s in samples):.2f})")
    print(f"z_range=({min(s['z'] for s in samples):.2f}, {max(s['z'] for s in samples):.2f})")


if __name__ == "__main__":
    main()
