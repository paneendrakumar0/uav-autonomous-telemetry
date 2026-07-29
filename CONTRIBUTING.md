# Contributing

This repository uses phase branches and pull requests to keep the research
history reviewable. Direct commits to `main` are not part of the normal
workflow.

## Branch workflow

1. Update the local default branch:

   ```bash
   git switch main
   git pull --ff-only origin main
   ```

2. Create a branch named for one research phase or engineering stage:

   ```bash
   git switch -c phase/<short-purpose>-YYYY-MM-DD
   ```

   Use `stage/<short-purpose>-YYYY-MM-DD` for commissioning or integration
   work that does not yet claim a research result.

3. Keep commits focused. Do not mix controller changes, experiment results,
   and unrelated cleanup in one commit.

4. Run the checks that apply to the change:

   ```bash
   python3 -m compileall -q tools tests ros2_ws/src/uav_control/launch
   python3 -m unittest discover -s tests -v
   ```

5. Push the branch and open a pull request:

   ```bash
   git push -u origin HEAD
   ```

6. Merge only after the pull request records the evidence and limitations.
   Prefer a merge commit so individual experimental commits remain traceable.
   Delete the remote branch after merging.

## Pull-request evidence

Every research pull request must state:

- the hypothesis or engineering objective;
- the controller, vehicle, payload, trajectory, and environment versions;
- independent variables, controlled variables, and validation gates;
- trial count and whether trial order or disturbances were randomized;
- retained raw-data and generated-artifact locations;
- numerical results with units;
- failures, outliers, and known limitations;
- exact commands used for validation.

Screening runs must be labelled as screening evidence. A single run must not be
presented as a repeatability or robustness result.

## Experiment data

New experiment runners must retain raw telemetry by default and write an
`experiment_manifest.json` beside the results. If raw telemetry is intentionally
excluded from Git because of size, archive it separately and record its checksum
and location in the pull request.

Do not rewrite published experiment history to improve a result. Corrections
must be added as new commits with an explanation.
