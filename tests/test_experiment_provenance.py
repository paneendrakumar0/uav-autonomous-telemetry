import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools"))

from experiment_provenance import (
    mark_raw_telemetry_discarded,
    relative_manifest_paths,
    write_manifest,
)


class ExperimentProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)

    def test_writes_shared_manifest_shape(self):
        snapshot = {
            "repository_commit": "abc123",
            "repository_branch": "phase/test",
            "repository_dirty": False,
            "px4_commit": "px4abc",
        }
        with patch("experiment_provenance.software_snapshot", return_value=snapshot):
            path = write_manifest(
                self.root,
                experiment_type="repeatability_validation",
                repo_root=REPO_ROOT,
                px4_dir=self.root / "px4",
                parameters={"trials_per_profile": 3},
                data={"raw_telemetry_retained": True},
                result={"valid_trials": 6},
            )

        manifest = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema_version"], 1)
        self.assertEqual(manifest["experiment"]["type"], "repeatability_validation")
        self.assertEqual(manifest["experiment"]["parameters"]["trials_per_profile"], 3)
        self.assertEqual(manifest["software"], snapshot)
        self.assertEqual(manifest["result"]["valid_trials"], 6)

    def test_lists_only_nested_manifests(self):
        (self.root / "experiment_manifest.json").write_text("{}\n", encoding="utf-8")
        nested = self.root / "case_a"
        nested.mkdir()
        (nested / "experiment_manifest.json").write_text("{}\n", encoding="utf-8")
        deeper = self.root / "case_b" / "trial_01"
        deeper.mkdir(parents=True)
        (deeper / "experiment_manifest.json").write_text("{}\n", encoding="utf-8")

        self.assertEqual(
            relative_manifest_paths(self.root),
            [
                "case_a/experiment_manifest.json",
                "case_b/trial_01/experiment_manifest.json",
            ],
        )

    def test_marks_discarded_raw_telemetry(self):
        path = self.root / "experiment_manifest.json"
        path.write_text(
            json.dumps({"schema_version": 1, "data": {"raw_telemetry_retained": True}}) + "\n",
            encoding="utf-8",
        )

        mark_raw_telemetry_discarded(
            self.root,
            ["tracking_metrics.csv", "payload_swing_metrics.csv"],
        )

        manifest = json.loads(path.read_text(encoding="utf-8"))
        self.assertFalse(manifest["data"]["raw_telemetry_retained"])
        self.assertEqual(
            manifest["data"]["discarded_raw_files"],
            ["payload_swing_metrics.csv", "tracking_metrics.csv"],
        )


if __name__ == "__main__":
    unittest.main()
