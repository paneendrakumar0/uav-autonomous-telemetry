#!/usr/bin/env python3
# tools/analyze_kinematics.py
# Computes maximum velocity and acceleration for lemniscate (Figure-8) trajectories
# based on amplitude A and angular frequency omega.

import math
import argparse

def compute_kinematics(A, omega):
    """
    Parametric peak derivations for the Figure-8:
    v_max = sqrt(5) * A * omega
    a_max = 4 * A * (omega^2)
    """
    v_max = math.sqrt(5) * A * omega
    a_max = 4 * A * (omega ** 2)
    return v_max, a_max

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate peak kinematics for Figure-8 trajectory")
    parser.add_argument("--amplitude", type=float, default=5.0, help="Trajectory amplitude in meters (default: 5.0)")
    parser.add_argument("--frequencies", type=str, default="0.15,0.20,0.25,0.30", help="Comma-separated omegas in rad/s")
    parser.add_argument("--markdown", action="store_true", help="Output as a Markdown table")
    
    args = parser.parse_args()
    omegas = [float(w.strip()) for w in args.frequencies.split(",")]
    
    if args.markdown:
        print(f"| $\\omega$ (rad/s) | $v_{{max}}$ (m/s) | $a_{{max}}$ (m/s$^2$) |")
        print(f"|---|---:|---:|")
        for omega in omegas:
            v_max, a_max = compute_kinematics(args.amplitude, omega)
            print(f"| {omega:.2f} | {v_max:.2f} | {a_max:.2f} |")
    else:
        print(f"Kinematic Analysis for Figure-8 (A = {args.amplitude} m)\n")
        print(f"{'Omega (rad/s)':<15} | {'v_max (m/s)':<15} | {'a_max (m/s^2)':<15}")
        print("-" * 50)
        for omega in omegas:
            v_max, a_max = compute_kinematics(args.amplitude, omega)
            print(f"{omega:<15.2f} | {v_max:<15.2f} | {a_max:<15.2f}")
