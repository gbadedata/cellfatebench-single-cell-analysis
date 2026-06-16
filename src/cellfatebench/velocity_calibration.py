"""Empirical calibration and difficulty rebalancing for CellFateBench v2."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd


DEFAULT_PUBLIC_TASKS_PATH = Path("benchmark_tasks/public/velocity_reasoning_tasks.json")
DEFAULT_TASK_PERFORMANCE_PATH = Path("results/tables/velocity_task_performance_summary.csv")

DEFAULT_CALIBRATION_LOG_PATH = Path(
    "benchmark_tasks/calibration_logs/empirical_velocity_calibration_log.json"
)
DEFAULT_REBALANCED_TABLE_PATH = Path("results/tables/velocity_task_difficulty_rebalanced.csv")
DEFAULT_REBALANCED_FIGURE_PATH = Path("results/figures/velocity_task_difficulty_rebalance.png")


def load_json(path: Path) -> Any:
    """Load JSON from disk."""
    return json.loads(path.read_text(encoding="utf-8"))


def recommend_difficulty(mean_score: float, pass_rate: float) -> str:
    """
    Recommend task difficulty from empirical solver-performance evidence.

    The thresholds are intentionally simple and transparent.
    """
    if pass_rate >= 0.80 and mean_score >= 0.80:
        return "easy"
    if pass_rate >= 0.50 and mean_score >= 0.60:
        return "medium"
    return "hard"


def recommend_action(declared_difficulty: str, recommended_difficulty: str) -> str:
    """Recommend whether the declared difficulty should change."""
    if declared_difficulty == recommended_difficulty:
        return "keep"

    return f"rebalance_from_{declared_difficulty}_to_{recommended_difficulty}"


def build_velocity_difficulty_rebalance_table(
    public_tasks_path: Path = DEFAULT_PUBLIC_TASKS_PATH,
    task_performance_path: Path = DEFAULT_TASK_PERFORMANCE_PATH,
) -> pd.DataFrame:
    """Build a task-level difficulty rebalancing table."""
    public_tasks = load_json(public_tasks_path)
    task_performance = pd.read_csv(task_performance_path)

    declared = pd.DataFrame(
        [
            {
                "task_id": task["task_id"],
                "declared_difficulty": task["difficulty"],
                "task_type": task["task_type"],
            }
            for task in public_tasks
        ]
    )

    merged = declared.merge(task_performance, on="task_id", how="left", validate="one_to_one")

    if merged[["mean_score", "pass_rate"]].isna().any().any():
        missing = merged.loc[
            merged[["mean_score", "pass_rate"]].isna().any(axis=1), "task_id"
        ].tolist()
        raise ValueError(
            "Missing solver-performance evidence for task(s): " + ", ".join(missing)
        )

    merged["recommended_difficulty"] = merged.apply(
        lambda row: recommend_difficulty(
            mean_score=float(row["mean_score"]),
            pass_rate=float(row["pass_rate"]),
        ),
        axis=1,
    )
    merged["recommended_action"] = merged.apply(
        lambda row: recommend_action(
            declared_difficulty=str(row["declared_difficulty"]),
            recommended_difficulty=str(row["recommended_difficulty"]),
        ),
        axis=1,
    )

    columns = [
        "task_id",
        "task_type",
        "declared_difficulty",
        "recommended_difficulty",
        "recommended_action",
        "mean_score",
        "pass_rate",
        "mean_overclaim_penalty",
    ]
    return merged[columns].sort_values("task_id")


def build_empirical_velocity_calibration_log(
    rebalance_table: pd.DataFrame,
) -> dict[str, Any]:
    """Build an empirical calibration log from rebalanced task evidence."""
    task_reviews = []

    for row in rebalance_table.to_dict(orient="records"):
        task_reviews.append(
            {
                "task_id": row["task_id"],
                "task_type": row["task_type"],
                "declared_difficulty": row["declared_difficulty"],
                "recommended_difficulty": row["recommended_difficulty"],
                "recommended_action": row["recommended_action"],
                "mean_score": float(row["mean_score"]),
                "pass_rate": float(row["pass_rate"]),
                "mean_overclaim_penalty": float(row["mean_overclaim_penalty"]),
                "interpretation": interpret_task_performance(
                    pass_rate=float(row["pass_rate"]),
                    mean_score=float(row["mean_score"]),
                    mean_overclaim_penalty=float(row["mean_overclaim_penalty"]),
                ),
            }
        )

    return {
        "calibration_type": "empirical_velocity_solver_profile_calibration",
        "empirical_frontier_model_calibration_claimed": False,
        "calibration_basis": (
            "Calibration is based on local sample solver profiles: oracle, strong, "
            "overclaiming, and weak solvers. It is not a claim of frontier-model calibration."
        ),
        "total_tasks_reviewed": int(len(task_reviews)),
        "difficulty_recommendation_counts": (
            rebalance_table["recommended_difficulty"].value_counts().sort_index().to_dict()
        ),
        "recommended_action_counts": (
            rebalance_table["recommended_action"].value_counts().sort_index().to_dict()
        ),
        "task_reviews": task_reviews,
    }


def interpret_task_performance(
    pass_rate: float,
    mean_score: float,
    mean_overclaim_penalty: float,
) -> str:
    """Produce a concise interpretation for task calibration evidence."""
    if mean_overclaim_penalty > 0.05:
        return "Task reveals overclaiming behaviour and should retain explicit uncertainty checks."
    if pass_rate >= 0.80 and mean_score >= 0.80:
        return "Task appears easy for current sample solvers and may be suitable as a warm-up item."
    if pass_rate < 0.50:
        return "Task appears challenging and should be reviewed for clarity before increasing difficulty."
    return "Task appears appropriately challenging under the current sample solver profiles."


def plot_difficulty_rebalance(rebalance_table: pd.DataFrame, output_path: Path) -> None:
    """Plot declared versus recommended difficulty counts."""
    counts = (
        rebalance_table.groupby(["declared_difficulty", "recommended_difficulty"])
        .size()
        .reset_index(name="count")
    )
    counts["label"] = (
        counts["declared_difficulty"] + " to " + counts["recommended_difficulty"]
    )

    figure, axis = plt.subplots(figsize=(9, 5))
    axis.bar(counts["label"], counts["count"])
    axis.set_ylabel("Task count")
    axis.set_xlabel("Difficulty transition")
    axis.set_title("Velocity task difficulty rebalancing")
    axis.tick_params(axis="x", rotation=30)
    figure.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=150)
    plt.close(figure)


def write_velocity_calibration_outputs(
    public_tasks_path: Path = DEFAULT_PUBLIC_TASKS_PATH,
    task_performance_path: Path = DEFAULT_TASK_PERFORMANCE_PATH,
    calibration_log_path: Path = DEFAULT_CALIBRATION_LOG_PATH,
    rebalance_table_path: Path = DEFAULT_REBALANCED_TABLE_PATH,
    rebalance_figure_path: Path = DEFAULT_REBALANCED_FIGURE_PATH,
) -> dict[str, Path]:
    """Write empirical velocity calibration outputs."""
    rebalance_table = build_velocity_difficulty_rebalance_table(
        public_tasks_path=public_tasks_path,
        task_performance_path=task_performance_path,
    )
    calibration_log = build_empirical_velocity_calibration_log(rebalance_table)

    calibration_log_path.parent.mkdir(parents=True, exist_ok=True)
    rebalance_table_path.parent.mkdir(parents=True, exist_ok=True)
    rebalance_figure_path.parent.mkdir(parents=True, exist_ok=True)

    rebalance_table.to_csv(rebalance_table_path, index=False)
    calibration_log_path.write_text(
        json.dumps(calibration_log, indent=2),
        encoding="utf-8",
    )
    plot_difficulty_rebalance(rebalance_table, rebalance_figure_path)

    return {
        "calibration_log": calibration_log_path,
        "rebalance_table": rebalance_table_path,
        "rebalance_figure": rebalance_figure_path,
    }
