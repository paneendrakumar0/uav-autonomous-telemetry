#!/usr/bin/env python3
"""
evaluate_reference_metrics.py
Parses the flight trajectory CSV and evaluates whether the steady-state 
mean 3D tracking error falls within the acceptable pass/fail tolerance.
"""

import sys
import argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description="Evaluate UAV trajectory tracking metrics.")
    parser.add_argument("--csv", required=True, help="Path to the metrics CSV file")
    parser.add_argument("--threshold", type=float, default=0.50, help="Maximum allowed mean 3D error (m)")
    parser.add_argument("--steady-start", type=float, default=25.0, help="Time (s) to begin steady-state evaluation")
    args = parser.parse_args()

    # ANSI color codes for terminal output
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    NC = '\033[0m'

    try:
        df = pd.read_csv(args.csv)
    except FileNotFoundError:
        print(f"{RED}[ERROR]{NC} Metrics file not found: {args.csv}")
        sys.exit(1)

    if 't_s' not in df.columns or 'error_norm' not in df.columns:
        print(f"{RED}[ERROR]{NC} CSV is missing required columns ('t_s', 'error_norm').")
        sys.exit(1)

    # Isolate steady-state data
    steady_state_df = df[df['t_s'] >= args.steady_start]
    
    if steady_state_df.empty:
        print(f"{RED}[ERROR]{NC} No data recorded after t = {args.steady_start}s.")
        sys.exit(1)

    mean_error = steady_state_df['error_norm'].mean()
    print(f"Post-{int(args.steady_start)}s Mean 3D Error: {mean_error:.3f} m (Threshold: {args.threshold} m)\n")

    if mean_error < args.threshold:
        print(f"  {GREEN}==> [PASS]{NC} Tracking error is within acceptable tolerance.")
        sys.exit(0)
    else:
        print(f"  {RED}==> [FAIL]{NC} Tracking error exceeds the allowable threshold.")
        sys.exit(1)

if __name__ == "__main__":
    main()
