"""Tests for CellFateBench v2 public RNA velocity pipeline orchestration."""

from __future__ import annotations

from cellfatebench.v2_pipeline import run_v2_pipeline, validate_v2_expected_outputs


def test_run_v2_pipeline_produces_expected_sections() -> None:
    outputs = run_v2_pipeline()

    expected_sections = {
        "velocity_dataset",
        "velocity_tasks",
        "velocity_solver_evaluation",
    }

    assert set(outputs) == expected_sections


def test_validate_v2_expected_outputs_after_pipeline() -> None:
    run_v2_pipeline()
    validation = validate_v2_expected_outputs()

    assert validation
    assert all(validation.values())
