"""Visual outputs and summary tables for CellFateBench."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import json

import matplotlib.pyplot as plt
import pandas as pd


PUBLIC_TASK_FILES = [
    "benchmark_tasks/public/trajectory_pseudotime_tasks.json",
    "benchmark_tasks/public/spatial_pattern_tasks.json",
    "benchmark_tasks/public/topological_persistence_tasks.json",
]


def load_all_public_tasks(paths: list[str] | None = None) -> list[dict[str, Any]]:
    """Load all public benchmark tasks."""

    task_paths = paths or PUBLIC_TASK_FILES
    tasks: list[dict[str, Any]] = []

    for path in task_paths:
        tasks.extend(json.loads(Path(path).read_text()))

    return tasks


def build_task_summary_table(
    output_path: str | Path = "results/tables/benchmark_task_summary.csv",
) -> str:
    """Create a compact benchmark task summary table."""

    tasks = load_all_public_tasks()

    rows = []
    for task in tasks:
        rows.append(
            {
                "task_id": task["task_id"],
                "task_family": task["task_family"],
                "difficulty": task["difficulty"],
                "question_length": len(task["question"]),
                "has_observable_data": "observable_data" in task,
                "answer_format_fields": len(task.get("answer_format", {})),
            }
        )

    table = pd.DataFrame(rows).sort_values(["task_family", "task_id"])
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(output_path, index=False)

    return str(output_path)


def save_synthetic_spatial_layout(
    output_path: str | Path = "results/figures/synthetic_spatial_layout.png",
) -> str:
    """Plot synthetic spatial coordinates coloured by hidden spatial domain."""

    metadata = pd.read_csv("data/synthetic/synthetic_cell_metadata.csv")

    fig, ax = plt.subplots(figsize=(8, 6))

    for domain, group in metadata.groupby("true_spatial_domain"):
        ax.scatter(
            group["spatial_x"],
            group["spatial_y"],
            s=14,
            alpha=0.75,
            label=domain,
        )

    ax.set_title("CellFateBench Synthetic Spatial Layout")
    ax.set_xlabel("spatial_x")
    ax.set_ylabel("spatial_y")
    ax.legend(fontsize=8, loc="best")
    fig.tight_layout()

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)

    return str(output_path)


def save_pseudotime_by_branch(
    output_path: str | Path = "results/figures/pseudotime_by_branch.png",
) -> str:
    """Plot pseudotime distribution by branch."""

    metadata = pd.read_csv("data/synthetic/synthetic_cell_metadata.csv")

    branch_order = ["root", "transition", "branch_a", "branch_b"]
    values = [
        metadata.loc[metadata["true_branch"] == branch, "true_pseudotime"].to_numpy()
        for branch in branch_order
    ]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.boxplot(values, labels=branch_order)
    ax.set_title("Pseudotime Distribution by Designed Branch")
    ax.set_xlabel("Designed branch")
    ax.set_ylabel("true_pseudotime")
    fig.tight_layout()

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)

    return str(output_path)


def save_task_family_counts(
    output_path: str | Path = "results/figures/task_family_counts.png",
) -> str:
    """Plot benchmark task counts by family."""

    tasks = load_all_public_tasks()
    table = pd.DataFrame(tasks)

    counts = table["task_family"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(counts.index, counts.values)
    ax.set_title("Benchmark Task Counts by Family")
    ax.set_xlabel("Task family")
    ax.set_ylabel("Number of public tasks")
    ax.tick_params(axis="x", rotation=25)
    fig.tight_layout()

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)

    return str(output_path)


def save_sample_solver_scores(
    output_path: str | Path = "results/figures/sample_solver_scores.png",
) -> str:
    """Plot sample solver score by task."""

    report = json.loads(Path("results/reports/sample_solver_score_report.json").read_text())
    rows = report["task_results"]

    table = pd.DataFrame(rows)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(table["task_id"], table["score"])
    ax.set_title("Sample Solver Scores by Task")
    ax.set_xlabel("Task ID")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 1.05)
    ax.tick_params(axis="x", rotation=75)
    fig.tight_layout()

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)

    return str(output_path)


def generate_all_visual_outputs() -> dict[str, str]:
    """Generate all reviewer-friendly summary tables and figures."""

    return {
        "task_summary_table": build_task_summary_table(),
        "synthetic_spatial_layout": save_synthetic_spatial_layout(),
        "pseudotime_by_branch": save_pseudotime_by_branch(),
        "task_family_counts": save_task_family_counts(),
        "sample_solver_scores": save_sample_solver_scores(),
    }
