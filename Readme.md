# Autonomous UAV Flight Pipeline & Telemetry Logger

This repository contains a ROS 2 (Humble) workspace for autonomous Unmanned Aerial Vehicle (UAV) control and telemetry data extraction. It interfaces directly with the PX4 Autopilot flight stack running in Software-In-The-Loop (SITL) mode within the Gazebo simulation environment.

## System Architecture
* **Flight Controller:** PX4 Autopilot (SITL)
* **Physics Simulator:** Gazebo Sim
* **UAV Model:** x500 Quadrotor
* **Middleware:** Micro-XRCE-DDS (DDS-XRCE protocol bridge)
* **Ground Control Station:** QGroundControl
* **Autonomy Stack:** ROS 2 Humble (C++)

## Features
* **Offboard Control Node:** Bypasses manual pilot inputs to arm the drone, transition to offboard flight mode, and execute autonomous 3D waypoint navigation (e.g., executing a 50x50m multi-lap circuit).
* **Telemetry Logger Node:** Subscribes to `/fmu/out/vehicle_odometry` using `SensorDataQoS` (Best Effort) policies to extract real-time flight data and log high-fidelity timestamps and X-Y-Z NED coordinates to a CSV file.
* **Trajectory Visualization:** Python-based post-flight analysis tool that converts raw CSV odometry into publication-ready 3D trajectory plots and 2D axis-vs-time graphs.

## Dependencies & Installation

### 1. PX4 Autopilot & Gazebo
Clone and build the official PX4 flight stack to enable SITL and the x500 Gazebo model.
```bash
git clone [https://github.com/PX4/PX4-Autopilot.git](https://github.com/PX4/PX4-Autopilot.git) --recursive
bash ./PX4-Autopilot/Tools/setup/ubuntu.sh
