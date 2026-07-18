#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline_csv', required=True)
    parser.add_argument('--geometric_csv', required=True)
    parser.add_argument('--baseline_swing', required=True)
    parser.add_argument('--geometric_swing', required=True)
    parser.add_argument('--out_dir', required=True)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df_base = pd.read_csv(args.baseline_csv).dropna()
    df_geom = pd.read_csv(args.geometric_csv).dropna()
    swing_base = pd.read_csv(args.baseline_swing).dropna()
    swing_geom = pd.read_csv(args.geometric_swing).dropna()

    # 1. XY Overlay
    plt.figure(figsize=(10, 10))
    plt.plot(df_base['actual_y'].to_numpy(), df_base['actual_x'].to_numpy(), label='PX4 Baseline', alpha=0.7)
    plt.plot(df_geom['actual_y'].to_numpy(), df_geom['actual_x'].to_numpy(), label='Geometric Controller', alpha=0.7)
    plt.plot(df_geom['reference_y'].to_numpy(), df_geom['reference_x'].to_numpy(), 'k--', label='Reference', alpha=0.5)
    plt.xlabel('Y (East) [m]')
    plt.ylabel('X (North) [m]')
    plt.title('Matched-Rate XY Tracking Comparison (omega=0.25)')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.savefig(out_dir / 'comparison_xy.png')
    plt.close()

    # 2. Tracking Error Over Time
    plt.figure(figsize=(10, 5))
    err_base = np.sqrt((df_base['actual_x'] - df_base['reference_x'])**2 + (df_base['actual_y'] - df_base['reference_y'])**2 + (df_base['actual_z'] - df_base['reference_z'])**2).to_numpy()
    err_geom = np.sqrt((df_geom['actual_x'] - df_geom['reference_x'])**2 + (df_geom['actual_y'] - df_geom['reference_y'])**2 + (df_geom['actual_z'] - df_geom['reference_z'])**2).to_numpy()
    
    t_base = (df_base['t_s'] - df_base['t_s'].iloc[0]).to_numpy()
    t_geom = (df_geom['t_s'] - df_geom['t_s'].iloc[0]).to_numpy()
    
    plt.plot(t_base, err_base, label='PX4 Baseline', alpha=0.7)
    plt.plot(t_geom, err_geom, label='Geometric Controller', alpha=0.7)
    plt.axvline(25, color='r', linestyle='--', label='Steady State t=25s')
    plt.xlabel('Time [s]')
    plt.ylabel('3D Tracking Error [m]')
    plt.title('Matched-Rate Tracking Error (omega=0.25)')
    plt.legend()
    plt.grid(True)
    plt.savefig(out_dir / 'comparison_error.png')
    plt.close()

    # 3. Cable Angle Over Time
    plt.figure(figsize=(10, 5))
    t_swing_base = (swing_base['t_s'] - swing_base['t_s'].iloc[0]).to_numpy()
    t_swing_geom = (swing_geom['t_s'] - swing_geom['t_s'].iloc[0]).to_numpy()
    plt.plot(t_swing_base, swing_base['cable_angle_deg'].to_numpy(), label='PX4 Baseline', alpha=0.7)
    plt.plot(t_swing_geom, swing_geom['cable_angle_deg'].to_numpy(), label='Geometric Controller', alpha=0.7)
    plt.axvline(25, color='r', linestyle='--', label='Steady State t=25s')
    plt.xlabel('Time [s]')
    plt.ylabel('Cable Angle [deg]')
    plt.title('Matched-Rate Payload Swing (omega=0.25)')
    plt.legend()
    plt.grid(True)
    plt.savefig(out_dir / 'comparison_cable_angle.png')
    plt.close()
    print(f"Comparison plots saved to {out_dir}")

if __name__ == "__main__":
    main()
