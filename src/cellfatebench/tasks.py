"""Benchmark task generation for CellFateBench.

This module builds public benchmark tasks, hidden answer keys, and oracle
outputs from the controlled synthetic single-cell dataset.

The first task family focuses on trajectory and pseudotime reasoning.
"""

from __future__ import annotations

from pathlib import Path
import json
from typing import Any

import pandas as pd


TRAJECTORY_TASK_FAMILY = "trajectory_pseudotime_reasoning"


def _load_synthetic_inputs(
    metadata_path: str | Path = "data/synthetic/synthetic_cell_metadata.csv",
    expression_path: str | Path = "data/synthetic/synthetic_expression_matrix.csv",
    gene_metadata_path: str | Path = "data/synthetic/synthetic_gene_metadata.csv",
    hidden_truth_path: str | Path = "data/synthetic/synthetic_hidden_truth.json",
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    metadata = pd.read_csv(metadata_path)
    expression = pd.read_csv(expression_path)
    gene_metadata = pd.read_csv(gene_metadata_path)
    hidden_truth = json.loads(Path(hidden_truth_path).read_text())
    return metadata, expression, gene_metadata, hidden_truth


def _mean_expression_by_state(metadata: pd.DataFrame, expression: pd.DataFrame) -> pd.DataFrame:
    merged = metadata[["cell_id", "true_state", "true_branch", "true_pseudotime"]].merge(
        expression,
        on="cell_id",
        how="inner",
    )
    gene_columns = [col for col in expression.columns if col != "cell_id"]
    return merged.groupby("true_state")[gene_columns].mean().round(4)


def _top_state_markers(
    metadata: pd.DataFrame,
    expression: pd.DataFrame,
    state: str,
    n_markers: int = 6,
) -> list[str]:
    merged = metadata[["cell_id", "true_state"]].merge(expression, on="cell_id", how="inner")
    gene_columns = [col for col in expression.columns if col != "cell_id"]

    state_mean = merged.loc[merged["true_state"] == state, gene_columns].mean()
    other_mean = merged.loc[merged["true_state"] != state, gene_columns].mean()
    delta = (state_mean - other_mean).sort_values(ascending=False)

    return [gene for gene in delta.head(n_markers).index.tolist()]


def _state_summary(metadata: pd.DataFrame, expression: pd.DataFrame) -> dict[str, Any]:
    states = sorted(metadata["true_state"].unique().tolist())
    summary: dict[str, Any] = {}

    for state in states:
        state_rows = metadata[metadata["true_state"] == state]
        summary[state] = {
            "n_cells": int(state_rows.shape[0]),
            "median_pseudotime": round(float(state_rows["true_pseudotime"].median()), 4),
            "pseudotime_range": [
                round(float(state_rows["true_pseudotime"].min()), 4),
                round(float(state_rows["true_pseudotime"].max()), 4),
            ],
            "top_markers": _top_state_markers(metadata, expression, state, n_markers=6),
        }

    return summary


def generate_trajectory_tasks(
    output_root: str | Path = "benchmark_tasks",
) -> dict[str, str]:
    """Generate trajectory/pseudotime public tasks, hidden answers, and oracle outputs."""

    metadata, expression, gene_metadata, hidden_truth = _load_synthetic_inputs()
    state_summary = _state_summary(metadata, expression)

    root_state = hidden_truth["trajectory_truth"]["root_state"]
    transition_state = hidden_truth["trajectory_truth"]["transition_state"]
    terminal_states = hidden_truth["trajectory_truth"]["terminal_states"]

    ordered_states = [
        root_state,
        transition_state,
        *terminal_states,
    ]

    public_tasks: list[dict[str, Any]] = []
    hidden_answers: list[dict[str, Any]] = []
    oracle_outputs: list[dict[str, Any]] = []

    task_1_id = "trajectory_root_state_inference_001"
    public_tasks.append(
        {
            "task_id": task_1_id,
            "task_family": TRAJECTORY_TASK_FAMILY,
            "difficulty": "medium",
            "question": (
                "Given the state-level pseudotime summaries and top marker genes, "
                "identify the most likely root/progenitor state in the trajectory."
            ),
            "observable_data": {
                state: {
                    "median_pseudotime": state_summary[state]["median_pseudotime"],
                    "pseudotime_range": state_summary[state]["pseudotime_range"],
                    "top_markers": state_summary[state]["top_markers"],
                }
                for state in ordered_states
            },
            "answer_format": {
                "root_state": "string",
                "supporting_evidence": "list of marker or pseudotime observations",
                "confidence": "low | medium | high",
            },
        }
    )
    hidden_answers.append(
        {
            "task_id": task_1_id,
            "expected_root_state": root_state,
            "acceptable_aliases": ["root_progenitor", "progenitor", "root"],
            "required_evidence_terms": ["lowest pseudotime", "ROOT", "early"],
        }
    )
    oracle_outputs.append(
        {
            "task_id": task_1_id,
            "oracle_answer": {
                "root_state": root_state,
                "confidence": "high",
                "rationale": (
                    "The root_progenitor state has the earliest pseudotime range and "
                    "is enriched for ROOT marker genes, making it the most plausible "
                    "starting state of the trajectory."
                ),
                "supporting_evidence": [
                    "lowest median pseudotime among states",
                    "enrichment of ROOT marker genes",
                    "position before transition and terminal states",
                ],
            },
        }
    )

    task_2_id = "trajectory_terminal_state_inference_002"
    public_tasks.append(
        {
            "task_id": task_2_id,
            "task_family": TRAJECTORY_TASK_FAMILY,
            "difficulty": "medium",
            "question": (
                "Using the pseudotime ranges and marker patterns, identify the two "
                "terminal states in the bifurcating trajectory."
            ),
            "observable_data": {
                state: {
                    "median_pseudotime": state_summary[state]["median_pseudotime"],
                    "pseudotime_range": state_summary[state]["pseudotime_range"],
                    "top_markers": state_summary[state]["top_markers"],
                }
                for state in ordered_states
            },
            "answer_format": {
                "terminal_states": "list of two strings",
                "supporting_evidence": "list of marker or pseudotime observations",
                "confidence": "low | medium | high",
            },
        }
    )
    hidden_answers.append(
        {
            "task_id": task_2_id,
            "expected_terminal_states": terminal_states,
            "acceptable_aliases": {
                "branch_a_terminal": ["branch_a_terminal", "A terminal", "branch A"],
                "branch_b_terminal": ["branch_b_terminal", "B terminal", "branch B"],
            },
            "required_evidence_terms": ["highest pseudotime", "A_TERM", "B_TERM", "terminal"],
        }
    )
    oracle_outputs.append(
        {
            "task_id": task_2_id,
            "oracle_answer": {
                "terminal_states": terminal_states,
                "confidence": "high",
                "rationale": (
                    "branch_a_terminal and branch_b_terminal occupy late pseudotime ranges "
                    "and show distinct terminal marker programs, indicating two terminal "
                    "branches in the trajectory."
                ),
                "supporting_evidence": [
                    "late pseudotime ranges",
                    "branch-specific A_TERM markers",
                    "branch-specific B_TERM markers",
                    "bifurcating trajectory structure",
                ],
            },
        }
    )

    task_3_id = "trajectory_transition_state_ordering_003"
    public_tasks.append(
        {
            "task_id": task_3_id,
            "task_family": TRAJECTORY_TASK_FAMILY,
            "difficulty": "hard",
            "question": (
                "Infer the most plausible ordering of cell states from early to late "
                "pseudotime. Explain where the transition state sits relative to the "
                "root and terminal states."
            ),
            "observable_data": {
                state: {
                    "median_pseudotime": state_summary[state]["median_pseudotime"],
                    "pseudotime_range": state_summary[state]["pseudotime_range"],
                    "top_markers": state_summary[state]["top_markers"],
                }
                for state in ordered_states
            },
            "answer_format": {
                "early_to_late_order": "list of state names",
                "branching_interpretation": "short explanation",
                "confidence": "low | medium | high",
            },
        }
    )
    hidden_answers.append(
        {
            "task_id": task_3_id,
            "expected_order": [root_state, transition_state, terminal_states],
            "expected_transition_state": transition_state,
            "required_evidence_terms": ["intermediate pseudotime", "TRANS", "between root and terminal"],
        }
    )
    oracle_outputs.append(
        {
            "task_id": task_3_id,
            "oracle_answer": {
                "early_to_late_order": [root_state, transition_state, terminal_states],
                "branching_interpretation": (
                    "The trajectory starts at root_progenitor, passes through an intermediate "
                    "transition_state, and then bifurcates into branch_a_terminal and "
                    "branch_b_terminal."
                ),
                "confidence": "high",
                "supporting_evidence": [
                    "root state has earliest pseudotime",
                    "transition state has intermediate pseudotime and TRANS markers",
                    "terminal states have late pseudotime and branch-specific markers",
                ],
            },
        }
    )

    task_4_id = "trajectory_masked_terminal_recovery_004"
    public_tasks.append(
        {
            "task_id": task_4_id,
            "task_family": TRAJECTORY_TASK_FAMILY,
            "difficulty": "hard",
            "question": (
                "One terminal branch label has been masked. Use the marker evidence and "
                "pseudotime range to recover the most likely hidden terminal identity."
            ),
            "observable_data": {
                "known_states": {
                    root_state: state_summary[root_state],
                    transition_state: state_summary[transition_state],
                    terminal_states[0]: state_summary[terminal_states[0]],
                },
                "masked_state": {
                    "state_name": "MASKED_TERMINAL_STATE",
                    "median_pseudotime": state_summary[terminal_states[1]]["median_pseudotime"],
                    "pseudotime_range": state_summary[terminal_states[1]]["pseudotime_range"],
                    "top_markers": state_summary[terminal_states[1]]["top_markers"],
                },
            },
            "answer_format": {
                "recovered_state": "string",
                "supporting_evidence": "list",
                "confidence": "low | medium | high",
            },
        }
    )
    hidden_answers.append(
        {
            "task_id": task_4_id,
            "expected_recovered_state": terminal_states[1],
            "required_evidence_terms": ["B_TERM", "late pseudotime", "terminal"],
        }
    )
    oracle_outputs.append(
        {
            "task_id": task_4_id,
            "oracle_answer": {
                "recovered_state": terminal_states[1],
                "confidence": "high",
                "rationale": (
                    "The masked state has late pseudotime and is enriched for B_TERM marker "
                    "genes, indicating that it corresponds to branch_b_terminal."
                ),
                "supporting_evidence": [
                    "late pseudotime range",
                    "B_TERM marker enrichment",
                    "distinct from branch_a_terminal marker program",
                ],
            },
        }
    )

    output_root = Path(output_root)
    public_dir = output_root / "public"
    hidden_dir = output_root / "hidden"
    oracle_dir = output_root / "oracle_outputs"

    public_dir.mkdir(parents=True, exist_ok=True)
    hidden_dir.mkdir(parents=True, exist_ok=True)
    oracle_dir.mkdir(parents=True, exist_ok=True)

    public_path = public_dir / "trajectory_pseudotime_tasks.json"
    hidden_path = hidden_dir / "trajectory_pseudotime_answers.json"
    oracle_path = oracle_dir / "trajectory_pseudotime_oracle_outputs.json"

    public_path.write_text(json.dumps(public_tasks, indent=2))
    hidden_path.write_text(json.dumps(hidden_answers, indent=2))
    oracle_path.write_text(json.dumps(oracle_outputs, indent=2))

    return {
        "public_tasks": str(public_path),
        "hidden_answers": str(hidden_path),
        "oracle_outputs": str(oracle_path),
    }
