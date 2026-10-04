#!/usr/bin/env python3
import sys
import pandas as pd

def evaluate_metrics(csv_path, max_error_threshold=0.50, steady_state_start=25.0):
    """
    Reads the tracking metrics CSV and evaluates whether the steady-state 
    mean tracking error falls within the acceptable tolerance.
    """
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"[ERROR] Metrics file not found: {csv_path}")
        return 1

    if 't_s' not in df.columns or 'error_norm' not in df.columns:
        print("[ERROR] CSV is missing required columns ('t_s', 'error_norm').")
        return 1

    # Filter for steady-state data
    steady_state_df = df[df['t_s'] >= steady_state_start]
    
    if steady_state_df.empty:
        print(f"[ERROR] No data recorded after t = {steady_state_start}s.")
        return 1

    mean_error = steady_state_df['error_norm'].mean()
    print(f"Post-{int(steady_state_start)}s Mean 3D Error: {mean_error:.3f} m")

    if mean_error < max_error_threshold:
        print(f"--> [PASS] Tracking error is within the {max_error_threshold} m tolerance.")
        return 0
    else:
        print(f"--> [FAIL] Tracking error exceeds the {max_error_threshold} m tolerance.")
        return 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 evaluate_reference_metrics.py <path_to_csv>")
        sys.exit(1)
    
    sys.exit(evaluate_metrics(sys.argv[1]))
