#!/usr/bin/env python3
"""
render_obstacle_animation.py
Renders a 3D animated video (.mp4) and GIF of the UAV + Slung Payload traversing 
the obstacle course (Pillar, Gate, Wall) using telemetry from obstacle_traversal_metrics.csv.
"""

import sys
import argparse
import csv
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter

def draw_cylinder(ax, center_x, center_y, radius, height, color='gray', alpha=0.7):
    z = np.linspace(0, height, 20)
    theta = np.linspace(0, 2*np.pi, 30)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x_grid = radius * np.cos(theta_grid) + center_x
    y_grid = radius * np.sin(theta_grid) + center_y
    ax.plot_surface(x_grid, y_grid, z_grid, color=color, alpha=alpha, shade=True)

def draw_wall(ax, x_pos, y_min, y_max, height, color='firebrick', alpha=0.6):
    y = np.linspace(y_min, y_max, 10)
    z = np.linspace(0, height, 10)
    y_grid, z_grid = np.meshgrid(y, z)
    x_grid = np.full_like(y_grid, x_pos)
    ax.plot_surface(x_grid, y_grid, z_grid, color=color, alpha=alpha, shade=True)

def main():
    parser = argparse.ArgumentParser(description="Render 3D flight animation video.")
    parser.add_argument("--csv", default="reports/obstacle_avoidance_run/obstacle_traversal_metrics.csv")
    parser.add_argument("--mp4", default="reports/obstacle_avoidance_run/obstacle_avoidance_flight.mp4")
    parser.add_argument("--gif", default="reports/obstacle_avoidance_run/obstacle_avoidance_flight.gif")
    parser.add_argument("--fps", type=int, default=20)
    args = parser.parse_args()

    rows = []
    try:
        with open(args.csv, "r") as f:
            reader = csv.DictReader(f)
            for r in reader:
                try:
                    rows.append({
                        "t": float(r["t_flight_s"]),
                        "x": float(r["uav_x"]),
                        "y": float(r["uav_y"]),
                        "z": -float(r["uav_z"]),  # Convert NED z to upward altitude
                        "vx": float(r["uav_vx"]),
                        "vy": float(r["uav_vy"]),
                        "vz": float(r["uav_vz"]),
                        "swing": float(r["swing_angle_deg"]),
                        "pillar_dist": float(r["dist_pillar1_m"]),
                        "gate_dist": float(r["dist_gate_m"]),
                    })
                except (ValueError, TypeError, KeyError):
                    continue
    except FileNotFoundError:
        print(f"[ERROR] Could not find {args.csv}")
        sys.exit(1)

    if not rows:
        print("[ERROR] No valid telemetry rows in CSV.")
        sys.exit(1)

    # Subsample to target fps (telemetry is logged at 20Hz)
    step = max(1, len(rows) // 250)  # Aim for ~250 frames for smooth rendering
    sampled = rows[::step]

    fig = plt.figure(figsize=(14, 7), dpi=120)
    ax3d = fig.add_subplot(121, projection="3d")
    ax_top = fig.add_subplot(122)

    # Static 3D Obstacle Environment
    def setup_3d_env(ax):
        ax.cla()
        draw_cylinder(ax, 5.0, 0.0, 0.4, 5.0, color='slategray', alpha=0.8) # Pillar 1
        draw_cylinder(ax, 10.0, 2.0, 0.4, 5.0, color='darkorange', alpha=0.8) # Gate left
        draw_cylinder(ax, 10.0, -2.0, 0.4, 5.0, color='darkorange', alpha=0.8) # Gate right
        draw_wall(ax, 15.0, -4.0, 4.0, 5.0, color='crimson', alpha=0.7) # Back wall

        ax.set_xlim([-1, 16])
        ax.set_ylim([-4, 4])
        ax.set_zlim([0, 5])
        ax.set_xlabel("X Forward [m]")
        ax.set_ylabel("Y Lateral [m]")
        ax.set_zlabel("Altitude [m]")
        ax.set_title("3D Payload-Aware Obstacle Traversal", fontsize=11, fontweight="bold")
        ax.view_init(elev=25, azim=-60)

    # Static 2D Top-Down Environment
    def setup_top_env(ax):
        ax.cla()
        # Pillar 1
        c1 = plt.Circle((5.0, 0.0), 0.4, color='slategray', label="Pillar 1")
        c1_safe = plt.Circle((5.0, 0.0), 0.9, color='slategray', fill=False, linestyle=":", label="Safety Boundary (0.5m)")
        ax.add_patch(c1)
        ax.add_patch(c1_safe)
        
        # Gate pillars
        cg1 = plt.Circle((10.0, 2.0), 0.4, color='darkorange', label="Gate Pillars")
        cg2 = plt.Circle((10.0, -2.0), 0.4, color='darkorange')
        ax.add_patch(cg1)
        ax.add_patch(cg2)
        
        # Wall
        ax.plot([15.0, 15.0], [-4.0, 4.0], color='crimson', linewidth=4, label="Boundary Wall")

        ax.set_xlim([-1, 16])
        ax.set_ylim([-4, 4])
        ax.set_aspect("equal")
        ax.set_xlabel("X Forward [m]")
        ax.set_ylabel("Y Lateral [m]")
        ax.set_title("Top-Down Navigation Radar (XY)", fontsize=11, fontweight="bold")
        ax.grid(True, alpha=0.3)

    setup_3d_env(ax3d)
    setup_top_env(ax_top)

    # Animated elements
    traj_3d, = ax3d.plot([], [], [], 'g-', linewidth=2.0, label="UAV Path")
    uav_3d, = ax3d.plot([], [], [], 'bo', markersize=8, label="UAV")
    cable_3d, = ax3d.plot([], [], [], 'k-', linewidth=1.5)
    payload_3d, = ax3d.plot([], [], [], 'ro', markersize=6, label="Slung Payload (1m)")

    traj_top, = ax_top.plot([], [], 'g-', linewidth=2.0, label="Flight Trajectory")
    uav_top, = ax_top.plot([], [], 'bo', markersize=8, label="UAV")
    payload_top, = ax_top.plot([], [], 'ro', markersize=6, label="Payload")

    hud_text = fig.text(0.5, 0.02, "", ha="center", fontsize=10, 
                        bbox=dict(boxstyle="round,pad=0.5", facecolor="wheat", alpha=0.5))

    L = 1.0  # Cable length

    def update(frame_idx):
        cur = sampled[frame_idx]
        past = sampled[:frame_idx+1]

        px = [r["x"] for r in past]
        py = [r["y"] for r in past]
        pz = [r["z"] for r in past]

        cx, cy, cz = cur["x"], cur["y"], cur["z"]
        
        # Calculate payload position from swing dynamics (small angle pendular kinematics)
        swing_rad = math.radians(cur["swing"])
        heading = math.atan2(cur["vy"], cur["vx"] if abs(cur["vx"]) > 1e-3 else 1e-3)
        pl_x = cx - L * math.sin(swing_rad) * math.cos(heading)
        pl_y = cy - L * math.sin(swing_rad) * math.sin(heading)
        pl_z = max(0.0, cz - L * math.cos(swing_rad))

        # Update 3D
        traj_3d.set_data(px, py)
        traj_3d.set_3d_properties(pz)

        uav_3d.set_data([cx], [cy])
        uav_3d.set_3d_properties([cz])

        cable_3d.set_data([cx, pl_x], [cy, pl_y])
        cable_3d.set_3d_properties([cz, pl_z])

        payload_3d.set_data([pl_x], [pl_y])
        payload_3d.set_3d_properties([pl_z])

        # Update Top-Down
        traj_top.set_data(px, py)
        uav_top.set_data([cx], [cy])
        payload_top.set_data([pl_x], [pl_y])

        v_mag = math.hypot(cur["vx"], cur["vy"])
        hud_text.set_text(
            f"T: {cur['t']:5.1f}s | Pos: ({cx:4.1f}, {cy:4.1f}, {cz:4.1f})m | "
            f"Vel: {v_mag:4.2f}m/s | Pillar Dist: {cur['pillar_dist']:4.2f}m | "
            f"Payload Swing: {cur['swing']:4.1f}° (Limit: <=15.0°)"
        )

        return traj_3d, uav_3d, cable_3d, payload_3d, traj_top, uav_top, payload_top, hud_text

    print(f"[INFO] Rendering {len(sampled)} animation frames...")
    anim = FuncAnimation(fig, update, frames=len(sampled), interval=1000//args.fps, blit=False)

    try:
        writer_mp4 = FFMpegWriter(fps=args.fps, metadata=dict(artist="Antigravity"), bitrate=1800)
        anim.save(args.mp4, writer=writer_mp4)
        print(f"[SUCCESS] High-definition MP4 video saved to: {args.mp4}")
    except Exception as e:
        print(f"[WARN] FFMpegWriter encountered: {e}. Falling back to GIF...")

    try:
        writer_gif = PillowWriter(fps=min(args.fps, 15))
        anim.save(args.gif, writer=writer_gif)
        print(f"[SUCCESS] Animated GIF saved to: {args.gif}")
    except Exception as e:
        print(f"[WARN] PillowWriter encountered: {e}")

if __name__ == "__main__":
    main()
