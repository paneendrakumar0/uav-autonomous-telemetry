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

2. Micro-XRCE-DDS Agent

Required to bridge uORB messages from PX4 to ROS 2 topics.
Bash

git clone [https://github.com/eProsima/Micro-XRCE-DDS-Agent.git](https://github.com/eProsima/Micro-XRCE-DDS-Agent.git)
cd Micro-XRCE-DDS-Agent
mkdir build && cd build
cmake ..
make
sudo make install
sudo ldconfig /usr/local/lib/

3. Python Analysis Tools

Ensure a compatible version of NumPy is installed alongside Matplotlib for trajectory generation.
Bash

pip3 install "numpy<2" matplotlib --force-reinstall

Launch Instructions

To execute the autonomous flight and record data, the system requires four distinct processes running simultaneously. Open four separate terminals:

Terminal 1: Physics Simulator
Bash

cd ~/PX4-Autopilot
make px4_sitl gz_x500

Terminal 2: DDS Bridge
Bash

MicroXRCEAgent udp4 -p 8888

Terminal 3: Telemetry Logger
Bash

cd ~/ros2_ws
source install/setup.zsh
ros2 run uav_control telemetry_logger

Terminal 4: Offboard Flight Execution
Bash

cd ~/ros2_ws
source install/setup.zsh
ros2 run uav_control offboard_control

Generating Results

Once the flight circuit is complete, safely terminate the logger using Ctrl+C. A flight_trajectory.csv file will be generated in the workspace root. Execute the plotting script to generate the visual report:
Bash

python3 plot_data.py

Future Work

    Slung Payload Integration: Modify the x500 .sdf model to append a physical cable and mass to simulate dynamic payload disturbances.

    Perception Baseline: Integrate Intel RealSense stereo-depth camera and IMU plugins for occupancy mapping.

    Convex MPC: Implement a Model Predictive Control pipeline for advanced trajectory optimization compensating for payload swing.


***

Once your code and documentation are safely pushed to GitHub, are you ready to open the Gazebo model files and tackle the physics for the slung payload?# Autonomous UAV Flight Pipeline & Telemetry Logger

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
