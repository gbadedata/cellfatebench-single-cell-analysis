"""Calibration and difficulty-review utilities for CellFateBench.

This module creates design-stage calibration assets for benchmark tasks.

The current calibration layer is intentionally honest: it documents expected
difficulty, reasoning requirements, leakage risks, likely solver failure modes,
and future model/human calibration needs. It does not claim empirical frontier
model calibration until such experiments are performed.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
import json


PUBLIC_TASK_FILES = [
    "benchmark_tasks/public/trajectory_pseudotime_tasks.json",
    "benchmark_tasks/public/spatial_pattern_tasks.json",
    "benchmark_tasks/public/topological_persistence_tasks.json",
]


def load_public_tasks(paths: list[str] | None = None) -> list[dict[str, Any]]:
    """Load all public benchmark tasks."""

    task_paths = paths or PUBLIC_TASK_FILES
    tasks: list[dict[str, Any]] = []

    for path in task_paths:
        tasks.extend(json.loads(Path(path).read_text()))

    return tasks


def infer_reasoning_requirements(task: dict[str, Any]) -> list[str]:
    """Infer high-level reasoning requirements from task metadata."""

    task_id = task["task_id"]
    task_family = task["task_family"]
    question = task["question"].lower()

    requirements: list[str] = []

    if task_family == "trajectory_pseudotime_reasoning":
        requirements.extend(["pseudotime interpretation", "cell-state ordering"])
        if "terminal" in question:
            requirements.append("terminal-state inference")
        if "masked" in str(task).lower():
            requirements.append("hidden-state recovery")

    if task_family == "spatial_pattern_reasoning":
        requirements.extend(["spatial-domain interpretation", "gene-pattern matching"])
        if "masked" in str(task).lower():
            requirements.append("hidden-spatial-domain recovery")
        if "false-positive" in question or "claim" in question:
            requirements.append("false-positive detection")

    if task_family == "topological_persistence_reasoning":
        requirements.extend(["topology-aware interpretation", "trajectory-vs-spatial disambiguation"])
        if "masked" in str(task).lower():
            requirements.append("hidden-topology recovery")
        if "false-positive" in question or "claim" in question:
            requirements.append("false-positive topology detection")

    return sorted(set(requirements))


def infer_likely_failure_modes(task: dict[str, Any]) -> list[str]:
    """Infer likely solver failure modes for a task."""

    task_id = task["task_id"]
    task_family = task["task_family"]

    failure_modes: list[str] = []

    if task_family == "trajectory_pseudotime_reasoning":
        failure_modes.extend([
            "selecting terminal states using marker names but ignoring pseudotime",
            "confusing transition state with terminal state",
            "giving a label without supporting marker or pseudotime evidence",
        ])

    if task_family == "spatial_pattern_reasoning":
        failure_modes.extend([
            "treating any high-expression gene as spatially variable",
            "confusing pseudotime-associated genes with spatial-domain markers",
            "failing to distinguish left/right/ring spatial programmes",
        ])

    if task_family == "topological_persistence_reasoning":
        failure_modes.extend([
            "confusing spatial ring signal with cyclic cell-fate trajectory",
            "over-interpreting persistence summaries without biological context",
            "ignoring branch-count evidence when inferring topology",
        ])

    if "masked" in str(task).lower():
        failure_modes.append("failing hidden-information recovery from partial evidence")

    if "false" in task_id or "false-positive" in task.get("question", "").lower():
        failure_modes.append("accepting an unsupported claim instead of rejecting it")

    return sorted(set(failure_modes))


def calibration_recommendation(task: dict[str, Any]) -> str:
    """Provide a calibration recommendation for a task."""

    difficulty = task.get("difficulty", "unknown")
    task_text = json.dumps(task).lower()

    if difficulty == "medium":
        return (
            "Use as an initial calibration task. Expected to be solvable by systems "
            "that combine domain markers with quantitative summaries."
        )

    if difficulty == "hard" and "masked" in task_text:
        return (
            "Use for hidden-information recovery calibration. Check whether solvers "
            "infer the missing state/domain/topology from evidence rather than guessing."
        )

    if difficulty == "hard" and ("false-positive" in task_text or "claim" in task_text):
        return (
            "Use for adversarial reasoning calibration. Check whether solvers reject "
            "unsupported interpretations instead of pattern-matching superficially."
        )

    return (
        "Review with model and human calibration runs. Update difficulty label after "
        "empirical solver performance is available."
    )


def build_calibration_log() -> dict[str, Any]:
    """Build a design-stage calibration log for all current benchmark tasks."""

    tasks = load_public_tasks()

    task_reviews = []
    for task in tasks:
        task_reviews.append(
            {
                "task_id": task["task_id"],
                "task_family": task["task_family"],
                "declared_difficulty": task.get("difficulty", "unknown"),
                "reasoning_requirements": infer_reasoning_requirements(task),
                "likely_failure_modes": infer_likely_failure_modes(task),
                "calibration_recommendation": calibration_recommendation(task),
                "empirical_calibration_status": "not_yet_run_against_frontier_models",
            }
        )

    family_counts: dict[str, int] = {}
    difficulty_counts: dict[str, int] = {}

    for task in tasks:
        family_counts[task["task_family"]] = family_counts.get(task["task_family"], 0) + 1
        difficulty_counts[task.get("difficulty", "unknown")] = difficulty_counts.get(task.get("difficulty", "unknown"), 0) + 1

    return {
        "calibration_type": "design_stage_calibration_review",
        "empirical_frontier_model_calibration_claimed": False,
        "total_tasks_reviewed": len(tasks),
        "task_family_counts": family_counts,
        "difficulty_counts": difficulty_counts,
        "calibration_note": (
            "This log documents design-stage difficulty and failure-mode review. "
            "It is not an empirical frontier-model calibration report."
        ),
        "task_reviews": task_reviews,
    }


def write_calibration_log(
    output_path: str | Path = "benchmark_tasks/calibration_logs/design_stage_calibration_log.json",
) -> str:
    """Write design-stage calibration log to disk."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    log = build_calibration_log()
    output_path.write_text(json.dumps(log, indent=2))

    return str(output_path)
