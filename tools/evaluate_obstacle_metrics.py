#!/usr/bin/env python3
"""
evaluate_obstacle_metrics.py
Evaluates UAV obstacle avoidance and payload swing damping performance.
Asserts obstacle clearance (>= 0.5m) and maximum payload swing (<= 15 deg).
"""

import sys
import argparse
import csv
import math

def main():
    parser = argparse.ArgumentParser(description="Evaluate obstacle course traversal metrics.")
    parser.add_argument("--csv", required=True, help="Path to obstacle traversal CSV file")
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
                        "z": float(r["uav_z"]),
                        "pillar1_dist": float(r["dist_pillar1_m"]),
                        "gate_dist": float(r["dist_gate_m"]),
                        "swing_deg": float(r["swing_angle_deg"]),
                    })
                except (ValueError, TypeError, KeyError):
                    continue
    except FileNotFoundError:
        print(f"[FAIL] Metrics file not found: {args.csv}")
        sys.exit(1)

    if not rows:
        print(f"[FAIL] No trajectory data found in {args.csv}")
        sys.exit(1)

    # Calculate key metrics
    flight_duration = max(r["t"] for r in rows)
    max_x = max(r["x"] for r in rows)
    max_swing = max(r["swing_deg"] for r in rows)
    mean_swing = sum(r["swing_deg"] for r in rows) / len(rows)

    # Pillar 1 is at (5.0, 0.0) with radius 0.4m.
    # Minimum distance to center:
    pillar1_clearances = [r["pillar1_dist"] for r in rows if 3.0 <= r["x"] <= 7.0]
    min_pillar1_dist = min(pillar1_clearances) if pillar1_clearances else 999.0
    net_pillar1_clearance = min_pillar1_dist - 0.4  # Subtract cylinder radius

    # Gate is at (10.0, +/-2.0) with gap at y=0
    gate_traversals = [abs(r["y"]) for r in rows if 9.0 <= r["x"] <= 11.0]
    max_gate_y_deviation = max(gate_traversals) if gate_traversals else 999.0

    print("==================================================")
    print(" OBSTACLE AVOIDANCE & SWING EVALUATION REPORT")
    print("==================================================")
    print(f"Flight Duration:         {flight_duration:.1f} s")
    print(f"Max Forward Progress:    {max_x:.2f} m (Wall at 15.0m)")
    print(f"Pillar 1 Net Clearance:  {net_pillar1_clearance:.2f} m (Safety requirement: >= 0.50m)")
    print(f"Gate Center Alignment:   |y| <= {max_gate_y_deviation:.2f} m (Opening width: 4.0m)")
    print(f"Peak Payload Swing:      {max_swing:.2f} deg (Safety requirement: <= 15.0 deg)")
    print(f"Mean Payload Swing:      {mean_swing:.2f} deg")
    print("--------------------------------------------------")

    passed = True
    reasons = []

    if net_pillar1_clearance < 0.50:
        passed = False
        reasons.append(f"Pillar clearance ({net_pillar1_clearance:.2f}m) < 0.50m threshold")

    if max_gate_y_deviation > 1.50:
        passed = False
        reasons.append(f"Gate deviation ({max_gate_y_deviation:.2f}m) exceeded corridor")

    if max_swing > 15.0:
        passed = False
        reasons.append(f"Peak payload swing ({max_swing:.2f} deg) exceeded 15.0 deg safety constraint")

    if max_x < 10.0:
        passed = False
        reasons.append(f"Vehicle did not reach gate (max_x = {max_x:.2f}m < 10.0m)")

    if passed:
        print("\033[32m[PASS]\033[0m Obstacle course successfully traversed with payload swing bounded <= 15 deg!")
        sys.exit(0)
    else:
        print(f"\033[31m[FAIL]\033[0m Verification failed: {', '.join(reasons)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
