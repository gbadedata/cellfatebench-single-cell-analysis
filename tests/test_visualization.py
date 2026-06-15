"""Tests for CellFateBench visual outputs."""

from pathlib import Path

import pandas as pd

from cellfatebench.visualization import (
    build_task_summary_table,
    generate_all_visual_outputs,
)


def test_build_task_summary_table(tmp_path: Path) -> None:
    output = build_task_summary_table(tmp_path / "task_summary.csv")

    table = pd.read_csv(output)

    assert table.shape[0] == 12
    assert set(table["task_family"]) == {
        "trajectory_pseudotime_reasoning",
        "spatial_pattern_reasoning",
        "topological_persistence_reasoning",
    }


def test_generate_all_visual_outputs(tmp_path: Path) -> None:
    outputs = generate_all_visual_outputs()

    expected_keys = {
        "task_summary_table",
        "synthetic_spatial_layout",
        "pseudotime_by_branch",
        "task_family_counts",
        "sample_solver_scores",
    }

    assert set(outputs) == expected_keys

    for path in outputs.values():
        assert Path(path).exists()
        assert Path(path).stat().st_size > 0
