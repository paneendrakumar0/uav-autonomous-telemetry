# Research Roadmap

## Current position

The repository contains a functioning PX4/ROS 2 slung-payload SITL platform,
a PX4 position/velocity baseline, a geometric attitude/thrust prototype, and
controlled Figure-8 evidence.

The strongest completed campaign is the 10 + 10 nominal repeatability set. It
shows that the tuned geometric controller reduces mean 3D tracking error by
23.68% and mean cable angle by 10.09% relative to the PX4 baseline at
`omega=0.25 rad/s`.

The speed, payload-parameter, and wind screenings identify important limits:

- PX4 tracks better at the two slowest tested trajectory rates.
- A `0.20 kg` payload exposes a tracking-versus-swing tradeoff.
- Constant crosswind causes a large steady tracking bias in the geometric
  controller even though its swing reduction remains visible.

These results make the project an evidence-backed simulation prototype. They do
not yet establish a payload-aware, disturbance-robust control contribution.

## Phase 1: Research hardening

Objective: make every new result traceable and independently reproducible.

Exit criteria:

- phase branches and pull-request evidence are used for all changes;
- analysis dependencies are versioned;
- metric calculations have automated tests;
- every new experiment writes software and parameter provenance;
- raw telemetry is retained or archived with checksums;
- simulator, PX4, ROS, `px4_msgs`, and project revisions are recorded;
- screening results are clearly separated from statistical campaigns.

## Phase 2: Payload-state feedback

Objective: close the controller loop around measured or estimated payload
motion.

Candidate work:

- estimate cable direction and angular rate in a consistent frame;
- time-align vehicle and payload measurements;
- add cable-angle and cable-rate feedback to the controller;
- log estimator residuals and latency;
- compare PX4 baseline, current geometric control, and payload-aware control.

Exit criteria:

- estimator accuracy is quantified against simulator ground truth;
- an ablation isolates the effect of payload feedback;
- nominal repeatability is at least as strong as the existing 10 + 10 set.

## Phase 3: Adaptation and disturbance rejection

Objective: remove the failure modes exposed by heavy payloads and steady wind.

Candidate work:

- integral or extended-state disturbance estimation for constant wind;
- online mass or thrust-scale estimation;
- gain scheduling across trajectory rate and payload mass;
- actuator saturation and estimator-failure safeguards.

Exit criteria:

- tracking and swing improve without tuning separately for every test point;
- performance is reported across randomized mass, wind, sensor-noise, and
  initial-swing conditions;
- failure boundaries and negative results are included.

## Phase 4: Modern simulation and statistical campaign

Objective: validate the contribution on a maintained simulator with uncertainty.

Exit criteria:

- the payload model runs in modern Gazebo with a supported PX4/ROS 2 stack;
- experiments use declared random seeds and randomized run order;
- at least 30 randomized trials are run for primary comparisons, unless a
  power analysis justifies another sample count;
- effect sizes and confidence intervals accompany mean and RMS metrics;
- raw data and scripts reproduce every paper figure and table.

## Phase 5: HIL and flight validation

Objective: demonstrate that the result survives the simulation-to-real gap.

Exit criteria:

- hardware-in-the-loop tests exercise timing, estimator, and failsafe behavior;
- tethered flight starts with conservative payload and speed limits;
- emergency stop, geofence, and loss-of-offboard behavior are verified;
- real-flight results are compared against SITL using the same metrics;
- the final report contains equations, stability/safety reasoning, ablations,
  limitations, and a reproducibility package.
