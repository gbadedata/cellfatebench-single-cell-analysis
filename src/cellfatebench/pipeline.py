"""Full CellFateBench pipeline orchestration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cellfatebench.synthetic import generate_synthetic_dataset
from cellfatebench.tasks import (
    generate_trajectory_tasks,
    generate_spatial_tasks,
    generate_topology_tasks,
)
from cellfatebench.topology import write_topology_summary
from cellfatebench.calibration import write_calibration_log
from cellfatebench.scoring import score_solver_answers


def run_full_pipeline() -> dict[str, Any]:
    """Run the complete CellFateBench benchmark generation pipeline."""

    outputs: dict[str, Any] = {}

    outputs["synthetic_dataset"] = generate_synthetic_dataset()
    outputs["trajectory_tasks"] = generate_trajectory_tasks()
    outputs["spatial_tasks"] = generate_spatial_tasks()
    outputs["topology_summary"] = write_topology_summary()
    outputs["topology_tasks"] = generate_topology_tasks()
    outputs["calibration_log"] = write_calibration_log()
    outputs["sample_scoring_report"] = score_solver_answers(
        "sample_solver_answers/sample_answers.json"
    )

    return outputs


def validate_expected_outputs() -> dict[str, bool]:
    """Validate that expected pipeline outputs exist."""

    expected_paths = [
        "data/synthetic/synthetic_cell_metadata.csv",
        "data/synthetic/synthetic_expression_matrix.csv",
        "data/synthetic/synthetic_gene_metadata.csv",
        "data/synthetic/synthetic_hidden_truth.json",
        "benchmark_tasks/public/trajectory_pseudotime_tasks.json",
        "benchmark_tasks/hidden/trajectory_pseudotime_answers.json",
        "benchmark_tasks/oracle_outputs/trajectory_pseudotime_oracle_outputs.json",
        "benchmark_tasks/public/spatial_pattern_tasks.json",
        "benchmark_tasks/hidden/spatial_pattern_answers.json",
        "benchmark_tasks/oracle_outputs/spatial_pattern_oracle_outputs.json",
        "results/tables/topology_summary.json",
        "benchmark_tasks/public/topological_persistence_tasks.json",
        "benchmark_tasks/hidden/topological_persistence_answers.json",
        "benchmark_tasks/oracle_outputs/topological_persistence_oracle_outputs.json",
        "benchmark_tasks/calibration_logs/design_stage_calibration_log.json",
        "results/reports/sample_solver_score_report.json",
    ]

    return {path: Path(path).exists() for path in expected_paths}
