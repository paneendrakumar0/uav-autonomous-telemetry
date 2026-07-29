#!/usr/bin/env python3
"""Shared provenance helpers for UAV simulation experiments."""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def git_value(repo_dir: Path, *args: str) -> str:
    if not repo_dir.is_dir():
        return "unavailable"
    result = subprocess.run(
        ["git", "-C", str(repo_dir), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    value = result.stdout.strip()
    return value if result.returncode == 0 and value else "unavailable"


def git_dirty(repo_dir: Path) -> bool | str:
    if not repo_dir.is_dir():
        return "unavailable"
    result = subprocess.run(
        ["git", "-C", str(repo_dir), "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return "unavailable"
    return bool(result.stdout.strip())


def software_snapshot(repo_root: Path, px4_dir: Path | None = None) -> dict[str, Any]:
    snapshot: dict[str, Any] = {
        "repository_commit": git_value(repo_root, "rev-parse", "HEAD"),
        "repository_branch": git_value(repo_root, "branch", "--show-current"),
        "repository_dirty": git_dirty(repo_root),
        "ros_distro": os.environ.get("ROS_DISTRO", "unavailable"),
        "python_version": platform.python_version(),
        "python_executable": sys.executable,
        "platform": platform.platform(),
    }
    if px4_dir is not None:
        snapshot["px4_commit"] = git_value(px4_dir, "rev-parse", "HEAD")
        snapshot["px4_dirty"] = git_dirty(px4_dir)
    return snapshot


def relative_manifest_paths(out_dir: Path) -> list[str]:
    return sorted(
        path.relative_to(out_dir).as_posix()
        for path in out_dir.rglob("experiment_manifest.json")
        if path != out_dir / "experiment_manifest.json"
    )


def mark_raw_telemetry_discarded(run_dir: Path, removed_files: list[str]) -> None:
    path = run_dir / "experiment_manifest.json"
    if not path.exists():
        return
    manifest = json.loads(path.read_text(encoding="utf-8"))
    data = manifest.setdefault("data", {})
    data["raw_telemetry_retained"] = False
    data["discarded_raw_files"] = sorted(removed_files)
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def write_manifest(
    out_dir: Path,
    *,
    experiment_type: str,
    repo_root: Path,
    px4_dir: Path | None,
    parameters: dict[str, Any],
    data: dict[str, Any],
    result: dict[str, Any],
) -> Path:
    manifest = {
        "schema_version": 1,
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "experiment": {
            "type": experiment_type,
            "parameters": parameters,
        },
        "software": software_snapshot(repo_root, px4_dir),
        "data": data,
        "result": result,
    }
    path = out_dir / "experiment_manifest.json"
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return path
