from __future__ import annotations

import pandas as pd

from cellfatebench.velocity_solver_evaluation import (
    build_solver_performance_summary,
    build_task_performance_summary,
    calculate_evidence_score,
    calculate_overclaim_penalty,
    score_velocity_answer,
    score_velocity_solver_profiles,
    write_velocity_performance_outputs,
)


def test_score_velocity_answer_rewards_correct_answer_and_evidence() -> None:
    answer = {
        "task_id": "velocity_root_direction_inference_001",
        "answer": "Ductal",
        "supporting_evidence": ["Ductal upstream progenitor not terminal"],
        "confidence": 0.8,
    }
    hidden = {
        "task_id": "velocity_root_direction_inference_001",
        "expected_answer": "Ductal",
        "required_evidence_terms": ["Ductal", "upstream", "progenitor", "terminal"],
    }

    score = score_velocity_answer(answer, hidden)

    assert score["score"] >= 0.9
    assert score["passed"] is True


def test_calculate_evidence_score_is_fractional() -> None:
    answer = {"supporting_evidence": ["Ductal upstream"]}
    hidden = {"required_evidence_terms": ["Ductal", "upstream", "terminal"]}

    assert calculate_evidence_score(answer, hidden) == 2 / 3


def test_calculate_overclaim_penalty_detects_unsupported_precision() -> None:
    answer = {"supporting_evidence": ["definitely proven for every cluster"]}

    assert calculate_overclaim_penalty(answer) == 0.15


def test_score_velocity_solver_profiles_returns_expected_columns() -> None:
    frame = score_velocity_solver_profiles()

    assert not frame.empty
    assert set(
        [
            "solver_name",
            "solver_type",
            "task_id",
            "score",
            "passed",
            "overclaim_penalty",
        ]
    ).issubset(frame.columns)


def test_solver_performance_summary_contains_solver_profiles() -> None:
    scored_answers = score_velocity_solver_profiles()
    summary = build_solver_performance_summary(scored_answers)

    assert set(summary["solver_name"]) == {
        "oracle_velocity_solver",
        "strong_velocity_solver",
        "overclaiming_velocity_solver",
        "weak_velocity_solver",
    }
    assert summary["mean_score"].between(0, 1).all()
    assert summary["pass_rate"].between(0, 1).all()


def test_task_performance_summary_contains_all_velocity_tasks() -> None:
    scored_answers = score_velocity_solver_profiles()
    summary = build_task_performance_summary(scored_answers)

    assert summary.shape[0] == 6
    assert summary["mean_score"].between(0, 1).all()
    assert summary["pass_rate"].between(0, 1).all()


def test_write_velocity_performance_outputs_creates_tables_and_figures(tmp_path) -> None:
    solver_performance_path = tmp_path / "solver_summary.csv"
    task_performance_path = tmp_path / "task_summary.csv"
    solver_figure_path = tmp_path / "solver.png"
    task_figure_path = tmp_path / "task.png"

    outputs = write_velocity_performance_outputs(
        solver_performance_path=solver_performance_path,
        task_performance_path=task_performance_path,
        solver_figure_path=solver_figure_path,
        task_figure_path=task_figure_path,
    )

    for path in outputs.values():
        assert path.exists()

    solver_summary = pd.read_csv(solver_performance_path)
    task_summary = pd.read_csv(task_performance_path)

    assert not solver_summary.empty
    assert not task_summary.empty
