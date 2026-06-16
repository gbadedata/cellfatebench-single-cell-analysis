"""CellFateBench v2 public RNA velocity pipeline orchestration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cellfatebench.public_velocity import write_velocity_dataset_outputs
from cellfatebench.velocity_tasks import write_velocity_task_files
from cellfatebench.velocity_solver_evaluation import write_velocity_performance_outputs


VELOCITY_DATASET_SUMMARY_PATH = Path("results/tables/velocity_dataset_summary.csv")
VELOCITY_LAYER_SUMMARY_PATH = Path("results/tables/velocity_layer_summary.csv")

VELOCITY_PUBLIC_TASKS_PATH = Path("benchmark_tasks/public/velocity_reasoning_tasks.json")
VELOCITY_HIDDEN_ANSWERS_PATH = Path("benchmark_tasks/hidden/velocity_reasoning_answers.json")
VELOCITY_ORACLE_OUTPUTS_PATH = Path(
    "benchmark_tasks/oracle_outputs/velocity_reasoning_oracle_outputs.json"
)


def load_scvelo_pancreas_dataset() -> Any:
    """
    Load the public scVelo pancreas dataset.

    Large raw public data are not committed to this repository. scVelo handles
    download or cached loading through its dataset interface.
    """
    try:
        import scvelo as scv
    except ImportError as exc:
        raise ImportError(
            "scvelo is required for CellFateBench v2. "
            "Install the project environment from environment.yml."
        ) from exc

    return scv.datasets.pancreas()


def prepare_velocity_dataset_outputs() -> tuple[Path, Path]:
    """Load the public velocity dataset and write lightweight summary outputs."""
    adata = load_scvelo_pancreas_dataset()

    return write_velocity_dataset_outputs(
        adata=adata,
        dataset_name="scvelo_pancreas",
        summary_output_path=VELOCITY_DATASET_SUMMARY_PATH,
        layer_output_path=VELOCITY_LAYER_SUMMARY_PATH,
    )


def run_v2_pipeline() -> dict[str, Any]:
    """Run the CellFateBench v2 public RNA velocity extension pipeline."""
    outputs: dict[str, Any] = {}

    outputs["velocity_dataset"] = prepare_velocity_dataset_outputs()
    outputs["velocity_tasks"] = write_velocity_task_files(
        public_output_path=VELOCITY_PUBLIC_TASKS_PATH,
        hidden_output_path=VELOCITY_HIDDEN_ANSWERS_PATH,
        oracle_output_path=VELOCITY_ORACLE_OUTPUTS_PATH,
    )
    outputs["velocity_solver_evaluation"] = write_velocity_performance_outputs()

    return outputs


def validate_v2_expected_outputs() -> dict[str, bool]:
    """Validate that expected v2 pipeline outputs exist."""
    expected_paths = [
        VELOCITY_DATASET_SUMMARY_PATH,
        VELOCITY_LAYER_SUMMARY_PATH,
        VELOCITY_PUBLIC_TASKS_PATH,
        VELOCITY_HIDDEN_ANSWERS_PATH,
        VELOCITY_ORACLE_OUTPUTS_PATH,
        Path("results/tables/velocity_solver_performance_summary.csv"),
        Path("results/tables/velocity_task_performance_summary.csv"),
        Path("results/figures/velocity_solver_score_by_profile.png"),
        Path("results/figures/velocity_task_pass_rate.png"),
    ]

    return {str(path): path.exists() for path in expected_paths}
