#!/usr/bin/env python3
"""
evaluate_reference_metrics.py
Evaluates steady-state tracking error from Figure-8 trajectory telemetry.
Asserts that post-25s mean 3D position error satisfies the required threshold.
"""

import sys
import argparse
import csv

def main():
    parser = argparse.ArgumentParser(description="Evaluate Figure-8 reference tracking metrics.")
    parser.add_argument("--csv", required=True, help="Path to metrics CSV file")
    parser.add_argument("--threshold", type=float, default=0.50, help="Maximum allowable mean 3D error (m)")
    parser.add_argument("--steady-start", type=float, default=25.0, help="Time (s) marking start of steady state")
    args = parser.parse_args()

    errors = []
    try:
        with open(args.csv, "r") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames or "t_s" not in reader.fieldnames or "error_norm" not in reader.fieldnames:
                print(f"[FAIL] Missing required columns in {args.csv}")
                sys.exit(1)

            for row in reader:
                try:
                    t = float(row["t_s"])
                    if t >= args.steady_start:
                        errors.append(float(row["error_norm"]))
                except (ValueError, TypeError, KeyError):
                    continue
    except FileNotFoundError:
        print(f"[FAIL] Metrics file not found: {args.csv}")
        sys.exit(1)

    if not errors:
        print(f"[FAIL] Not enough steady-state data collected past {args.steady_start} seconds.")
        sys.exit(1)

    mean_error = sum(errors) / len(errors)
    print(f"Post-{int(args.steady_start)}s Mean 3D Tracking Error: {mean_error:.3f} m")

    if mean_error < args.threshold:
        print(f"\033[32m[PASS]\033[0m Error {mean_error:.3f} m is < {args.threshold:.2f} m threshold.")
        sys.exit(0)
    else:
        print(f"\033[31m[FAIL]\033[0m Error {mean_error:.3f} m exceeds {args.threshold:.2f} m threshold.")
        sys.exit(1)

if __name__ == "__main__":
    main()
