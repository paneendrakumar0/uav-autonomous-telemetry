import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools"))

from run_single_validation import summarize_swing, validate_tracking, write_experiment_manifest


def write_csv(path, fieldnames, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class TrackingValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)

    def write_tracking(self, actual_z=-5.0):
        path = self.root / "tracking.csv"
        rows = []
        for index, error in enumerate((0.5, 0.4, 0.3, 0.2)):
            rows.append(
                {
                    "t_s": 25.0 + index,
                    "actual_x": 1.0,
                    "actual_y": -1.0,
                    "actual_z": actual_z,
                    "error_x": error,
                    "error_y": 0.0,
                    "error_norm": error,
                }
            )
        write_csv(path, list(rows[0]), rows)
        return path

    def test_accepts_valid_tracking_and_calculates_metrics(self):
        valid, reason, metrics = validate_tracking(
            self.write_tracking(),
            min_samples=4,
            max_abs_position_m=100.0,
            target_altitude_ned=-5.0,
            max_mean_altitude_error_m=1.0,
        )

        self.assertTrue(valid)
        self.assertEqual(reason, "valid tracking telemetry")
        self.assertEqual(metrics["samples"], 4)
        self.assertAlmostEqual(metrics["mean_3d_error_m"], 0.35)
        self.assertAlmostEqual(metrics["mean_altitude_error_m"], 0.0)

    def test_rejects_insufficient_samples(self):
        valid, reason, metrics = validate_tracking(
            self.write_tracking(),
            min_samples=5,
            max_abs_position_m=100.0,
            target_altitude_ned=-5.0,
            max_mean_altitude_error_m=1.0,
        )

        self.assertFalse(valid)
        self.assertIn("too few tracking samples", reason)
        self.assertEqual(metrics["samples"], 4)

    def test_rejects_altitude_failure(self):
        valid, reason, metrics = validate_tracking(
            self.write_tracking(actual_z=-2.0),
            min_samples=4,
            max_abs_position_m=100.0,
            target_altitude_ned=-5.0,
            max_mean_altitude_error_m=1.0,
        )

        self.assertFalse(valid)
        self.assertIn("mean altitude error too large", reason)
        self.assertAlmostEqual(metrics["mean_altitude_error_m"], 3.0)

    def test_summarizes_payload_swing(self):
        path = self.root / "swing.csv"
        rows = [
            {
                "t_s": 25.0,
                "pose_source": "gazebo_same_frame",
                "cable_length_m": 1.0,
                "lateral_swing_m": 0.4,
                "cable_angle_deg": 20.0,
            },
            {
                "t_s": 26.0,
                "pose_source": "gazebo_same_frame",
                "cable_length_m": 1.0,
                "lateral_swing_m": 0.6,
                "cable_angle_deg": 30.0,
            },
        ]
        write_csv(path, list(rows[0]), rows)

        metrics = summarize_swing(path)

        self.assertTrue(metrics["swing_valid"])
        self.assertEqual(metrics["pose_source"], "gazebo_same_frame")
        self.assertAlmostEqual(metrics["mean_lateral_swing_m"], 0.5)
        self.assertAlmostEqual(metrics["mean_cable_angle_deg"], 25.0)

    def test_writes_versioned_experiment_manifest(self):
        args = SimpleNamespace(
            profile="geometric",
            launch_file="geometric_figure8_experiment.launch.py",
            world="payload_crosswind_y5",
            flight_duration_s=90.0,
            sitl_startup_s=20.0,
            omega=0.25,
            hover_thrust=0.72,
            min_samples=500,
            max_abs_position_m=100.0,
            target_altitude_ned=-5.0,
            max_mean_altitude_error_m=1.0,
        )
        summary = {
            "tracking_valid": True,
            "tracking_reason": "valid tracking telemetry",
            "swing_valid": True,
            "swing_reason": "valid payload swing telemetry",
        }

        with (
            patch("run_single_validation.git_value", side_effect=["repository-sha", "px4-sha"]),
            patch("run_single_validation.git_dirty", return_value=False),
        ):
            write_experiment_manifest(
                self.root,
                args,
                REPO_ROOT,
                self.root / "px4",
                summary,
            )

        manifest = json.loads((self.root / "experiment_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema_version"], 1)
        self.assertEqual(manifest["experiment"]["profile"], "geometric")
        self.assertEqual(manifest["experiment"]["parameters"]["omega_rad_s"], 0.25)
        self.assertEqual(manifest["software"]["repository_commit"], "repository-sha")
        self.assertEqual(manifest["software"]["px4_commit"], "px4-sha")
        self.assertFalse(manifest["software"]["repository_dirty"])
        self.assertTrue(manifest["data"]["raw_telemetry_retained"])


if __name__ == "__main__":
    unittest.main()
