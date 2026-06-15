"""Tests for full CellFateBench pipeline orchestration."""

from cellfatebench.pipeline import run_full_pipeline, validate_expected_outputs


def test_run_full_pipeline_produces_expected_sections() -> None:
    outputs = run_full_pipeline()

    expected_sections = {
        "synthetic_dataset",
        "trajectory_tasks",
        "spatial_tasks",
        "topology_summary",
        "topology_tasks",
        "calibration_log",
        "sample_scoring_report",
    }

    assert set(outputs) == expected_sections


def test_validate_expected_outputs_after_pipeline() -> None:
    run_full_pipeline()
    validation = validate_expected_outputs()

    assert validation
    assert all(validation.values())
