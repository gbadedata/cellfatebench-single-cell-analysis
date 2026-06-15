"""Tests for CellFateBench calibration logs."""

import json
from pathlib import Path

from cellfatebench.calibration import build_calibration_log, write_calibration_log


def test_build_calibration_log_reviews_all_tasks() -> None:
    log = build_calibration_log()

    assert log["calibration_type"] == "design_stage_calibration_review"
    assert log["empirical_frontier_model_calibration_claimed"] is False
    assert log["total_tasks_reviewed"] == 12
    assert log["task_family_counts"]["trajectory_pseudotime_reasoning"] == 4
    assert log["task_family_counts"]["spatial_pattern_reasoning"] == 4
    assert log["task_family_counts"]["topological_persistence_reasoning"] == 4


def test_calibration_log_contains_failure_modes() -> None:
    log = build_calibration_log()

    reviews = log["task_reviews"]
    assert len(reviews) == 12

    for review in reviews:
        assert review["reasoning_requirements"]
        assert review["likely_failure_modes"]
        assert review["empirical_calibration_status"] == "not_yet_run_against_frontier_models"


def test_write_calibration_log(tmp_path: Path) -> None:
    output = write_calibration_log(tmp_path / "calibration_log.json")
    log = json.loads(Path(output).read_text())

    assert log["total_tasks_reviewed"] == 12
    assert "calibration_note" in log
