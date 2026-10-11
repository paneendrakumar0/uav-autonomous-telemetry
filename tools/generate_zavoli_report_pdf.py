#!/usr/bin/env python3
"""
generate_zavoli_report_pdf.py
Compiles an academic, publication-grade PDF report responding to 
Professor Alessandro Zavoli's feedback on the UAV Slung-Payload project.
"""

import os
from weasyprint import HTML

def generate_report():
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    img_tracking = os.path.join(repo_dir, "reports/speed_sweep_validation_2026-07-22/speed_sweep_tracking_swing.png")
    img_improvement = os.path.join(repo_dir, "reports/speed_sweep_validation_2026-07-22/speed_sweep_improvement.png")
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Technical Report: UAV Slung-Payload SITL Evaluation</title>
<style>
    @page {{
        size: A4;
        margin: 20mm 18mm 20mm 18mm;
        @bottom-right {{
            content: "Page " counter(page) " of " counter(pages);
            font-size: 8pt;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            color: #7f8c8d;
        }}
        @bottom-left {{
            content: "Sapienza University of Rome — Flight Dynamics Feedback Response";
            font-size: 8pt;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            color: #7f8c8d;
        }}
    }}

    body {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 9.5pt;
        line-height: 1.5;
        color: #2c3e50;
    }}

    .header-box {{
        border-bottom: 2px solid #2980b9;
        padding-bottom: 12px;
        margin-bottom: 18px;
    }}

    .doc-title {{
        font-size: 18pt;
        font-weight: 700;
        color: #1a365d;
        margin: 0 0 6px 0;
    }}

    .doc-subtitle {{
        font-size: 11pt;
        font-weight: 500;
        color: #4a5568;
        margin: 0 0 10px 0;
    }}

    .meta-table {{
        width: 100%;
        font-size: 8.5pt;
        color: #4a5568;
        margin-top: 8px;
    }}

    .meta-table td {{
        padding: 2px 0;
        vertical-align: top;
    }}

    h2 {{
        font-size: 12pt;
        font-weight: 700;
        color: #1a365d;
        border-bottom: 1px solid #cbd5e0;
        padding-bottom: 4px;
        margin-top: 18px;
        margin-bottom: 8px;
        page-break-after: avoid;
    }}

    h3 {{
        font-size: 10pt;
        font-weight: 600;
        color: #2b6cb0;
        margin-top: 12px;
        margin-bottom: 6px;
        page-break-after: avoid;
    }}

    p {{
        margin: 0 0 8px 0;
        text-align: justify;
    }}

    table.data-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0;
        font-size: 8.5pt;
        page-break-inside: avoid;
    }}

    table.data-table th {{
        background-color: #2b6cb0;
        color: #ffffff;
        font-weight: 600;
        text-align: center;
        padding: 6px 8px;
        border: 1px solid #2b6cb0;
    }}

    table.data-table td {{
        padding: 5px 8px;
        border: 1px solid #e2e8f0;
        text-align: center;
    }}

    table.data-table tr:nth-child(even) {{
        background-color: #f7fafc;
    }}

    .badge-pass {{
        background-color: #27ae60;
        color: white;
        padding: 2px 6px;
        border-radius: 3px;
        font-weight: bold;
        font-size: 8pt;
    }}

    .code-box {{
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 3px solid #2b6cb0;
        padding: 8px 12px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 8pt;
        color: #1a202c;
        margin: 8px 0;
        line-height: 1.4;
        page-break-inside: avoid;
    }}

    .figure-container {{
        text-align: center;
        margin: 12px 0;
        page-break-inside: avoid;
    }}

    .figure-container img {{
        max-width: 95%;
        height: auto;
        border: 1px solid #e2e8f0;
        border-radius: 4px;
    }}

    .caption {{
        font-size: 8pt;
        color: #718096;
        margin-top: 4px;
        font-style: italic;
    }}

    .callout {{
        background-color: #ebf8ff;
        border-left: 3px solid #3182ce;
        padding: 8px 12px;
        margin: 10px 0;
        font-size: 9pt;
        page-break-inside: avoid;
    }}

    .page-break {{
        page-break-before: always;
    }}
</style>
</head>
<body>

<div class="header-box">
    <div class="doc-title">UAV Slung-Payload SITL: Technical Evaluation Report</div>
    <div class="doc-subtitle">Kinematic Aggressiveness vs. Bandwidth Interpretation & Environment Reproducibility</div>
    <table class="meta-table">
        <tr>
            <td style="width: 50%;"><strong>Author:</strong> Bathala Paneendra Kumar (NIT Durgapur)</td>
            <td style="width: 50%;"><strong>Recipient:</strong> Prof. Alessandro Zavoli & Fabio Polese</td>
        </tr>
        <tr>
            <td><strong>Project:</strong> Autonomous UAV with Slung Payload</td>
            <td><strong>Affiliation:</strong> Sapienza - University of Rome / NIT Durgapur</td>
        </tr>
        <tr>
            <td><strong>Repository:</strong> <a href="https://github.com/paneendrakumar0/uav-autonomous-telemetry" style="color: #2b6cb0; text-decoration: none;">github.com/paneendrakumar0/uav-autonomous-telemetry</a></td>
            <td><strong>Date:</strong> October 11, 2026</td>
        </tr>
    </table>
</div>

<h2>1. Executive Summary</h2>
<p>
This technical report addresses the constructive feedback provided by <strong>Professor Alessandro Zavoli</strong> regarding the UAV Slung-Payload Simulation-in-the-Loop (SITL) project. Specifically, this document:
</p>
<ul>
    <li>Calculates the analytical kinematic characteristics (peak velocity $v_{{max}}$ and peak acceleration $a_{{max}}$) of the commanded reference trajectory.</li>
    <li>Distinguishes whether tracking degradation across trajectory rates is driven by <em>trajectory aggressiveness</em> or <em>controller bandwidth / tuning</em>.</li>
    <li>Presents the containerized Docker and VS Code DevContainer architecture ensuring 1-command reproducibility for student researchers.</li>
    <li>Documents the automated reference test case with empirical tolerances and metrics.</li>
</ul>

<h2>2. Kinematic Aggressiveness vs. Controller Bandwidth</h2>
<p>
The reference Figure-8 path is parameterized in the horizontal plane with amplitude $A = 5.0\text{{ m}}$ and angular frequency $\omega\text{{ [rad/s]}}$:
</p>
<div style="text-align: center; margin: 6px 0; font-weight: bold;">
    $x(t) = A \sin(\omega t), \quad y(t) = A \sin(2\omega t), \quad z(t) = -2.5\text{{ m}}$
</div>
<p>
Differentiating analytically with respect to time yields the peak kinematic demands:
</p>
<ul>
    <li><strong>Maximum Commanded Velocity:</strong> $v_{{max}} = \sqrt{{5}} \cdot A \cdot \omega \approx 2.236 \cdot A \cdot \omega$</li>
    <li><strong>Maximum Commanded Acceleration:</strong> $a_{{max}} = 4 \cdot A \cdot \omega^2$</li>
</ul>

<p>
Table 1 summarizes the commanded kinematics alongside the steady-state tracking error and payload swing metrics obtained across three randomized trials per rate.
</p>

<table class="data-table">
    <thead>
        <tr>
            <th>Rate $\omega$ (rad/s)</th>
            <th>$v_{{max}}$ (m/s)</th>
            <th>$a_{{max}}$ (m/s²)</th>
            <th>Baseline 3D Error (m)</th>
            <th>Geometric 3D Error (m)</th>
            <th>Tracking Improvement</th>
            <th>Mean Swing Angle</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>0.15</strong></td>
            <td>1.68</td>
            <td>0.45</td>
            <td>0.179</td>
            <td>0.220</td>
            <td style="color: #c0392b;">-23.1%</td>
            <td>20.90°</td>
        </tr>
        <tr>
            <td><strong>0.20</strong></td>
            <td>2.24</td>
            <td>0.80</td>
            <td>0.283</td>
            <td>0.313</td>
            <td style="color: #c0392b;">-10.6%</td>
            <td>26.17°</td>
        </tr>
        <tr>
            <td><strong>0.25</strong></td>
            <td>2.80</td>
            <td>1.25</td>
            <td>0.446</td>
            <td>0.339</td>
            <td style="color: #27ae60; font-weight: bold;">+24.0%</td>
            <td>31.15°</td>
        </tr>
        <tr>
            <td><strong>0.30</strong></td>
            <td>3.35</td>
            <td>1.80</td>
            <td>0.676</td>
            <td>0.384</td>
            <td style="color: #27ae60; font-weight: bold;">+43.2%</td>
            <td>36.07°</td>
        </tr>
    </tbody>
</table>

<div class="callout">
    <strong>Key Analytical Findings:</strong>
    <br>
    <strong>1. Low-Speed Regime ($\omega \le 0.20\text{{ rad/s}}$):</strong> At $\omega = 0.15$, required acceleration is very modest ($a_{{max}} = 0.45\text{{ m/s}}^2$). The fact that the baseline PX4 controller outperforms the geometric controller here demonstrates a <strong>controller tuning / bandwidth trade-off</strong>. The geometric attitude gains were optimized for strong dynamic disturbance rejection, causing mild over-correction in slow, quasi-static conditions.
    <br><br>
    <strong>2. High-Speed Regime ($\omega \ge 0.25\text{{ rad/s}}$):</strong> Because commanded acceleration scales quadratically ($\propto \omega^2$), $a_{{max}}$ reaches $1.80\text{{ m/s}}^2$ at $\omega = 0.30$. In this regime, tracking errors grow across both architectures due to <strong>trajectory aggressiveness</strong> pushing against physical rotor thrust and vehicle tilt bounds. However, the geometric controller maintains higher effective bandwidth under heavy dynamic coupling, delivering a <strong>43.2% error reduction</strong> and a <strong>12.9% reduction in payload swing</strong> over the baseline.
</div>

<div class="figure-container">
    <img src="file://{img_improvement}" alt="Controller Improvement vs Rate">
    <div class="caption">Figure 1: Percentage improvement of geometric controller over PX4 baseline across commanded trajectory rates. Note the crossover to positive advantage at $\omega \ge 0.23\text{{ rad/s}}$.</div>
</div>

<div class="page-break"></div>

<div class="figure-container">
    <img src="file://{img_tracking}" alt="Tracking Error and Swing Comparison">
    <div class="caption">Figure 2: Absolute 3D position tracking error (left) and cable swing angle (right) as a function of trajectory rate $\omega$.</div>
</div>

<h2>3. Software Environment Reproducibility</h2>
<p>
To ensure seamless reproduction for student researchers without dependency conflicts, the repository provides fully pinned environments and automated testing.
</p>

<h3>3.1 Pinned Dependency Version Matrix</h3>
<table class="data-table">
    <thead>
        <tr>
            <th>Component</th>
            <th>Pinned Version / Branch</th>
            <th>Role in System</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>ROS 2</strong></td>
            <td>Humble Hawksbill (Desktop)</td>
            <td>Middleware, high-level geometric control & telemetry logging</td>
        </tr>
        <tr>
            <td><strong>Gazebo</strong></td>
            <td>Classic 11.10.2</td>
            <td>ODE physics engine (250 Hz step), slung-payload dynamics simulation</td>
        </tr>
        <tr>
            <td><strong>PX4 Autopilot</strong></td>
            <td>v1.15.2 (git tag)</td>
            <td>SITL autopilot firmware, EKF2 state estimation</td>
        </tr>
        <tr>
            <td><strong>Micro XRCE-DDS Agent</strong></td>
            <td>v2.4.2 (git tag)</td>
            <td>High-throughput client-to-agent bridge between PX4 uORB and ROS 2</td>
        </tr>
        <tr>
            <td><strong>px4_msgs</strong></td>
            <td>release/1.15 (git branch)</td>
            <td>Interface definitions for ROS 2 offboard control modes and setpoints</td>
        </tr>
    </tbody>
</table>

<h3>3.2 One-Command Reference Reproduction</h3>
<p>
Starting from a clean Linux machine with Docker installed, executing the following two commands automatically compiles and evaluates the reference Figure-8 trial:
</p>

<div class="code-box">
# 1. Clone repository and build Docker image<br>
git clone https://github.com/paneendrakumar0/uav-autonomous-telemetry.git<br>
cd uav-autonomous-telemetry<br>
docker build -t uav-payload-sitl .<br>
<br>
# 2. Run the automated reference test (headless)<br>
docker run --rm -v $(pwd):/workspaces/uav-autonomous-telemetry \<br>
&nbsp;&nbsp;-w /workspaces/uav-autonomous-telemetry uav-payload-sitl ./run_reference_test.sh
</div>

<h3>3.3 Pre-Defined Acceptance Tolerances & Empirical Results</h3>
<p>
The reference script (<code>run_reference_test.sh</code>) launches PX4 SITL and the ROS 2 controller at $\omega = 0.25\text{{ rad/s}}$. Once steady-state flight is reached ($t \ge 25\text{{ s}}$), the test evaluates position error against a strict acceptance gate:
</p>

<div class="code-box">
==========================================<br>
 UAV Slung-Payload Automated Reference Test<br>
==========================================<br>
[1/4] Starting Micro XRCE-DDS Agent...<br>
[2/4] Starting PX4 SITL (Headless)...<br>
[3/4] Launching ROS 2 offboard control (omega=0.25)...<br>
Waiting 85 seconds for experiment to collect steady-state data...<br>
[4/4] Cleaning up processes...<br>
==========================================<br>
 Analyzing Metrics<br>
==========================================<br>
Post-25s Mean 3D Tracking Error: 0.406 m<br>
<span style="color: #27ae60; font-weight: bold;">[PASS]</span> Error 0.406 m is &lt; 0.50 m threshold.
</div>

<h2>4. Current Research Progress: Payload-Aware Convex MPC</h2>
<p>
Following these reproducibility improvements, research has advanced to 3D obstacle avoidance using a <strong>Payload-Aware Convex Model Predictive Controller (MPC)</strong>:
</p>
<ul>
    <li><strong>Coupled Dynamics:</strong> Linearized 10-state space ($A_d, B_d$) capturing quadrotor kinematics and pendulum swing ($\ddot{{\theta}} \approx -(g/L)\theta - (1/L)a_{{xy}}$).</li>
    <li><strong>Safety Damping:</strong> Strict constraint on payload swing angle ($\theta_{{swing}} \le 15^\circ$) during evasive maneuvers.</li>
    <li><strong>Benchmark World:</strong> Integrated realistic asphalt runway, 5m cylindrical pillars, 4m wide gap gate, and terminal deceleration barrier.</li>
    <li><strong>Experimental Validation:</strong> Obstacle avoidance achieved with <strong>1.59m clearance</strong> at Pillar 1 and peak payload swing dampened to <strong>4.15°</strong> (well below the 15° threshold).</li>
</ul>

</body>
</html>
"""

    output_pdf = os.path.join(repo_dir, "reports/UAV_Slung_Payload_Zavoli_Feedback_Report.pdf")
    root_pdf = os.path.join(repo_dir, "UAV_Slung_Payload_Zavoli_Feedback_Report.pdf")
    
    HTML(string=html_content).write_pdf(output_pdf)
    HTML(string=html_content).write_pdf(root_pdf)
    
    print(f"Generated PDF Report at:")
    print(f"  - {output_pdf}")
    print(f"  - {root_pdf}")

if __name__ == "__main__":
    generate_report()
