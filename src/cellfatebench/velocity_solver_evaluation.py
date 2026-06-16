"""Velocity solver evaluation utilities for CellFateBench v2."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd


DEFAULT_SOLVER_PROFILE_PATH = Path("sample_solver_answers/velocity_solver_profiles.json")
DEFAULT_HIDDEN_ANSWER_PATH = Path("benchmark_tasks/hidden/velocity_reasoning_answers.json")

DEFAULT_SOLVER_PERFORMANCE_PATH = Path("results/tables/velocity_solver_performance_summary.csv")
DEFAULT_TASK_PERFORMANCE_PATH = Path("results/tables/velocity_task_performance_summary.csv")

DEFAULT_SOLVER_FIGURE_PATH = Path("results/figures/velocity_solver_score_by_profile.png")
DEFAULT_TASK_FIGURE_PATH = Path("results/figures/velocity_task_pass_rate.png")


def load_json(path: Path) -> Any:
    """Load JSON content from disk."""
    return json.loads(path.read_text(encoding="utf-8"))


def normalise_text(value: Any) -> str:
    """Normalise a value for forgiving evidence-term matching."""
    if isinstance(value, list):
        return " ".join(normalise_text(item) for item in value)
    if isinstance(value, dict):
        return " ".join(f"{key} {normalise_text(val)}" for key, val in value.items())
    return str(value).lower()


def answer_matches_expected(answer: dict[str, Any], hidden_answer: dict[str, Any]) -> bool:
    """Check whether a solver answer matches the main hidden expected answer."""
    if "expected_boolean_claim" in hidden_answer:
        if "accept_claim" not in answer:
            return False
        return bool(answer["accept_claim"]) is bool(hidden_answer["expected_boolean_claim"])

    expected = hidden_answer.get("expected_answer")
    accepted_answers = hidden_answer.get("accepted_answers", [])

    candidate_values = [
        answer.get("answer"),
        answer.get("ordered_groups"),
        answer.get("terminal_fates"),
        answer.get("failure_mode"),
    ]

    for candidate in candidate_values:
        if candidate is None:
            continue

        if candidate == expected:
            return True

        if candidate in accepted_answers:
            return True

        if isinstance(candidate, list) and isinstance(expected, list):
            if set(str(item) for item in candidate) == set(str(item) for item in expected):
                return True

        if isinstance(candidate, str) and isinstance(expected, str):
            if candidate.strip().lower() == expected.strip().lower():
                return True

    return False


def calculate_evidence_score(answer: dict[str, Any], hidden_answer: dict[str, Any]) -> float:
    """Calculate evidence-term coverage as a fraction between 0 and 1."""
    required_terms = hidden_answer.get("required_evidence_terms", [])
    if not required_terms:
        return 1.0

    answer_text = normalise_text(answer)
    matched_terms = [
        term for term in required_terms if str(term).lower() in answer_text
    ]

    return len(matched_terms) / len(required_terms)


def calculate_uncertainty_score(answer: dict[str, Any]) -> float:
    """Reward calibrated confidence reporting without requiring a specific value."""
    confidence = answer.get("confidence")
    if confidence is None:
        return 0.0

    try:
        confidence_value = float(confidence)
    except (TypeError, ValueError):
        return 0.0

    if 0 <= confidence_value <= 1:
        return 1.0

    return 0.0


def calculate_overclaim_penalty(answer: dict[str, Any]) -> float:
    """Apply a penalty when an answer claims unsupported precision."""
    answer_text = normalise_text(answer)

    overclaim_terms = [
        "definitely",
        "proves precise velocity",
        "every cluster",
        "fully proven",
        "no uncertainty",
        "guaranteed",
    ]

    if any(term in answer_text for term in overclaim_terms):
        return 0.15

    return 0.0


def score_velocity_answer(answer: dict[str, Any], hidden_answer: dict[str, Any]) -> dict[str, Any]:
    """
    Score one velocity reasoning answer.

    Rubric:
    - answer correctness: 0.40
    - evidence support: 0.30
    - uncertainty discipline: 0.20
    - no-overclaim discipline: 0.10
    """
    correctness_component = 0.40 if answer_matches_expected(answer, hidden_answer) else 0.0
    evidence_component = 0.30 * calculate_evidence_score(answer, hidden_answer)
    uncertainty_component = 0.20 * calculate_uncertainty_score(answer)
    overclaim_penalty = calculate_overclaim_penalty(answer)
    no_overclaim_component = 0.10 if overclaim_penalty == 0 else 0.0

    total_score = correctness_component + evidence_component + uncertainty_component + no_overclaim_component
    total_score = max(0.0, min(1.0, total_score - overclaim_penalty))

    return {
        "task_id": hidden_answer["task_id"],
        "score": round(total_score, 3),
        "passed": total_score >= 0.70,
        "correctness_component": round(correctness_component, 3),
        "evidence_component": round(evidence_component, 3),
        "uncertainty_component": round(uncertainty_component, 3),
        "no_overclaim_component": round(no_overclaim_component, 3),
        "overclaim_penalty": round(overclaim_penalty, 3),
    }


def score_velocity_solver_profiles(
    solver_profiles_path: Path = DEFAULT_SOLVER_PROFILE_PATH,
    hidden_answers_path: Path = DEFAULT_HIDDEN_ANSWER_PATH,
) -> pd.DataFrame:
    """Score all configured velocity solver profiles."""
    solver_profiles = load_json(solver_profiles_path)
    hidden_answers = load_json(hidden_answers_path)
    hidden_by_task = {answer["task_id"]: answer for answer in hidden_answers}

    records: list[dict[str, Any]] = []

    for profile in solver_profiles:
        solver_name = profile["solver_name"]
        solver_type = profile["solver_type"]

        for answer in profile["answers"]:
            task_id = answer["task_id"]
            hidden_answer = hidden_by_task[task_id]
            score_record = score_velocity_answer(answer, hidden_answer)

            records.append(
                {
                    "solver_name": solver_name,
                    "solver_type": solver_type,
                    **score_record,
                }
            )

    return pd.DataFrame(records)


def build_solver_performance_summary(scored_answers: pd.DataFrame) -> pd.DataFrame:
    """Build solver-level performance summary table."""
    summary = (
        scored_answers.groupby(["solver_name", "solver_type"], as_index=False)
        .agg(
            mean_score=("score", "mean"),
            passed_tasks=("passed", "sum"),
            total_tasks=("task_id", "count"),
            mean_overclaim_penalty=("overclaim_penalty", "mean"),
        )
    )
    summary["pass_rate"] = summary["passed_tasks"] / summary["total_tasks"]
    summary["mean_score"] = summary["mean_score"].round(3)
    summary["pass_rate"] = summary["pass_rate"].round(3)
    summary["mean_overclaim_penalty"] = summary["mean_overclaim_penalty"].round(3)
    return summary.sort_values(["mean_score", "pass_rate"], ascending=False)


def build_task_performance_summary(scored_answers: pd.DataFrame) -> pd.DataFrame:
    """Build task-level performance summary table."""
    summary = (
        scored_answers.groupby("task_id", as_index=False)
        .agg(
            mean_score=("score", "mean"),
            pass_rate=("passed", "mean"),
            mean_overclaim_penalty=("overclaim_penalty", "mean"),
        )
    )
    summary["mean_score"] = summary["mean_score"].round(3)
    summary["pass_rate"] = summary["pass_rate"].round(3)
    summary["mean_overclaim_penalty"] = summary["mean_overclaim_penalty"].round(3)
    return summary.sort_values("task_id")


def write_velocity_performance_outputs(
    solver_profiles_path: Path = DEFAULT_SOLVER_PROFILE_PATH,
    hidden_answers_path: Path = DEFAULT_HIDDEN_ANSWER_PATH,
    solver_performance_path: Path = DEFAULT_SOLVER_PERFORMANCE_PATH,
    task_performance_path: Path = DEFAULT_TASK_PERFORMANCE_PATH,
    solver_figure_path: Path = DEFAULT_SOLVER_FIGURE_PATH,
    task_figure_path: Path = DEFAULT_TASK_FIGURE_PATH,
) -> dict[str, Path]:
    """Score velocity solver profiles and write dashboard-ready outputs."""
    scored_answers = score_velocity_solver_profiles(
        solver_profiles_path=solver_profiles_path,
        hidden_answers_path=hidden_answers_path,
    )
    solver_summary = build_solver_performance_summary(scored_answers)
    task_summary = build_task_performance_summary(scored_answers)

    solver_performance_path.parent.mkdir(parents=True, exist_ok=True)
    task_performance_path.parent.mkdir(parents=True, exist_ok=True)
    solver_figure_path.parent.mkdir(parents=True, exist_ok=True)
    task_figure_path.parent.mkdir(parents=True, exist_ok=True)

    solver_summary.to_csv(solver_performance_path, index=False)
    task_summary.to_csv(task_performance_path, index=False)

    plot_solver_performance(solver_summary, solver_figure_path)
    plot_task_pass_rate(task_summary, task_figure_path)

    return {
        "solver_performance": solver_performance_path,
        "task_performance": task_performance_path,
        "solver_figure": solver_figure_path,
        "task_figure": task_figure_path,
    }


def plot_solver_performance(solver_summary: pd.DataFrame, output_path: Path) -> None:
    """Plot mean velocity benchmark score by solver profile."""
    figure, axis = plt.subplots(figsize=(9, 5))
    axis.bar(solver_summary["solver_name"], solver_summary["mean_score"])
    axis.set_ylim(0, 1)
    axis.set_ylabel("Mean score")
    axis.set_xlabel("Solver profile")
    axis.set_title("Velocity benchmark mean score by solver profile")
    axis.tick_params(axis="x", rotation=30)
    figure.tight_layout()
    figure.savefig(output_path, dpi=150)
    plt.close(figure)


def plot_task_pass_rate(task_summary: pd.DataFrame, output_path: Path) -> None:
    """Plot pass rate by velocity reasoning task."""
    figure, axis = plt.subplots(figsize=(10, 5))
    axis.bar(task_summary["task_id"], task_summary["pass_rate"])
    axis.set_ylim(0, 1)
    axis.set_ylabel("Pass rate")
    axis.set_xlabel("Task")
    axis.set_title("Velocity benchmark pass rate by task")
    axis.tick_params(axis="x", rotation=45)
    figure.tight_layout()
    figure.savefig(output_path, dpi=150)
    plt.close(figure)
