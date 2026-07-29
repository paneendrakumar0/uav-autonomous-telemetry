# Experiment Provenance

New validation campaigns write `experiment_manifest.json` into their output
directory. The manifest is intended to make a numerical result traceable to the
software, parameters, and retained evidence that produced it.

## Manifest structure

- `schema_version`: manifest format version.
- `created_at`: timezone-aware completion timestamp.
- `experiment.type`: stable runner identifier.
- `experiment.parameters`: controller, trajectory, validation, and campaign
  inputs.
- `software`: project branch and commit, dirty-worktree status, PX4 commit,
  ROS distribution, Python version, executable, and host platform.
- `data`: raw-data retention state and the names of summary artifacts.
- `result`: validity counts or gates appropriate to the campaign.

Batch manifests also list nested `experiment_manifest.json` files in
`data.constituent_manifests`. This connects an aggregate claim to its individual
trials.

## Raw telemetry policy

Repeatability, speed, payload-parameter, and wind campaigns retain raw tracking
and payload-swing CSV files by default. This is the publication-oriented mode.

To intentionally reduce repository size, pass:

```bash
--discard-raw-telemetry
```

When raw files are discarded, the constituent manifest is updated with
`raw_telemetry_retained: false` and records the filenames that were removed.
The pull request must identify any external archive and checksums used to
preserve those files.

## Provenance scope

The manifest records software and command-level provenance. It does not replace:

- PX4 ULog or ROS bag capture for high-fidelity debugging;
- checksums for externally archived raw data;
- declared random seeds and run randomization;
- calibration records;
- hardware serial numbers and firmware hashes for HIL or flight experiments.

Those fields can be added in a later schema version without changing historical
manifests.
