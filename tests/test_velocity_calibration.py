from __future__ import annotations

import json

import pandas as pd

from cellfatebench.velocity_calibration import (
    build_empirical_velocity_calibration_log,
    build_velocity_difficulty_rebalance_table,
    interpret_task_performance,
    recommend_action,
    recommend_difficulty,
    write_velocity_calibration_outputs,
)


def test_recommend_difficulty_uses_transparent_thresholds() -> None:
    assert recommend_difficulty(mean_score=0.9, pass_rate=0.9) == "easy"
    assert recommend_difficulty(mean_score=0.7, pass_rate=0.6) == "medium"
    assert recommend_difficulty(mean_score=0.4, pass_rate=0.25) == "hard"


def test_recommend_action_keeps_matching_difficulty() -> None:
    assert recommend_action("medium", "medium") == "keep"
    assert recommend_action("medium", "hard") == "rebalance_from_medium_to_hard"


def test_build_velocity_difficulty_rebalance_table_has_expected_columns() -> None:
    table = build_velocity_difficulty_rebalance_table()

    expected_columns = {
        "task_id",
        "task_type",
        "declared_difficulty",
        "recommended_difficulty",
        "recommended_action",
        "mean_score",
        "pass_rate",
        "mean_overclaim_penalty",
    }

    assert table.shape[0] == 6
    assert set(table.columns) == expected_columns
    assert table["recommended_difficulty"].isin(["easy", "medium", "hard"]).all()


def test_build_empirical_velocity_calibration_log_is_honest_about_scope() -> None:
    table = build_velocity_difficulty_rebalance_table()
    log = build_empirical_velocity_calibration_log(table)

    assert log["calibration_type"] == "empirical_velocity_solver_profile_calibration"
    assert log["empirical_frontier_model_calibration_claimed"] is False
    assert log["total_tasks_reviewed"] == 6
    assert len(log["task_reviews"]) == 6


def test_interpret_task_performance_mentions_overclaiming_when_penalty_is_high() -> None:
    interpretation = interpret_task_performance(
        pass_rate=0.75,
        mean_score=0.7,
        mean_overclaim_penalty=0.1,
    )

    assert "overclaiming" in interpretation


def test_write_velocity_calibration_outputs_creates_files(tmp_path) -> None:
    calibration_path = tmp_path / "calibration.json"
    table_path = tmp_path / "rebalance.csv"
    figure_path = tmp_path / "rebalance.png"

    outputs = write_velocity_calibration_outputs(
        calibration_log_path=calibration_path,
        rebalance_table_path=table_path,
        rebalance_figure_path=figure_path,
    )

    for path in outputs.values():
        assert path.exists()

    calibration = json.loads(calibration_path.read_text())
    table = pd.read_csv(table_path)

    assert calibration["total_tasks_reviewed"] == 6
    assert table.shape[0] == 6
