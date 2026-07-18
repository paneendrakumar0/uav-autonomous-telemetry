#!/usr/bin/env python3
import pandas as pd
import numpy as np
import scipy.stats as st
from pathlib import Path

def main():
    base_dir = Path("/home/paneendra/uav-autonomous-telemetry/reports/batch_testing")
    
    all_errors = []
    
    for i in range(1, 49):
        trial_dir = base_dir / f"trial_{i:02d}"
        csv_path = trial_dir / "figure8_tracking_metrics.csv"
        
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            # Filter for post-25s
            post_25 = df[df["t_s"] > 25.0]
            all_errors.extend(post_25["error_norm"].tolist())
            
    if not all_errors:
        print("No data found!")
        return
        
    all_errors = np.array(all_errors)
    
    mean = np.mean(all_errors)
    var = np.var(all_errors, ddof=1)
    std = np.std(all_errors, ddof=1)
    
    # 95% confidence interval
    # We can compute it over the data points or assuming a large sample
    # Using scipy.stats.t.interval
    ci = st.t.interval(0.95, len(all_errors)-1, loc=mean, scale=st.sem(all_errors))
    
    report = f"""# Batch Testing Aggregation Report

**Total Trials Analyzed**: 48
**Total Data Points (post-25s)**: {len(all_errors)}

## Tracking Error Metrics
* **Mean**: {mean:.4f} m
* **Variance**: {var:.6f} m^2
* **Standard Deviation**: {std:.4f} m
* **95% Confidence Interval**: ({ci[0]:.4f} m, {ci[1]:.4f} m)
"""
    
    print(report)
    
    report_path = base_dir / "aggregated_report.md"
    with open(report_path, "w") as f:
        f.write(report)
        
    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    main()
