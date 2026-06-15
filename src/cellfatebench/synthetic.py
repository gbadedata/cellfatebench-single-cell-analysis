"""Synthetic single-cell benchmark dataset generation.

This module creates controlled single-cell scenarios with known hidden truth for:
- trajectory and pseudotime reasoning;
- spatial pattern reasoning;
- topology-aware reasoning.

The goal is not to perfectly simulate all biology. The goal is to create an
evaluable benchmark dataset where hidden ground truth is known and validators
can score solver answers deterministically.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class SyntheticDatasetConfig:
    """Configuration for the controlled synthetic benchmark dataset."""

    n_root_cells: int = 220
    n_branch_a_cells: int = 240
    n_branch_b_cells: int = 240
    n_transition_cells: int = 200
    n_genes: int = 60
    random_seed: int = 42


GENE_GROUPS = {
    "root_state": ["ROOT1", "ROOT2", "ROOT3", "ROOT4", "ROOT5"],
    "transition_state": ["TRANS1", "TRANS2", "TRANS3", "TRANS4", "TRANS5"],
    "branch_a_terminal": ["A_TERM1", "A_TERM2", "A_TERM3", "A_TERM4", "A_TERM5"],
    "branch_b_terminal": ["B_TERM1", "B_TERM2", "B_TERM3", "B_TERM4", "B_TERM5"],
    "cycling": ["CYCLE1", "CYCLE2", "CYCLE3", "CYCLE4"],
    "spatial_domain_left": ["LEFT1", "LEFT2", "LEFT3"],
    "spatial_domain_right": ["RIGHT1", "RIGHT2", "RIGHT3"],
    "spatial_ring": ["RING1", "RING2", "RING3"],
}


def _all_gene_names(n_genes: int) -> list[str]:
    named_genes = [gene for genes in GENE_GROUPS.values() for gene in genes]
    filler_count = n_genes - len(named_genes)
    if filler_count < 0:
        raise ValueError("n_genes is smaller than the number of named marker genes.")
    return named_genes + [f"NOISE{i:02d}" for i in range(1, filler_count + 1)]


def _make_cell_metadata(config: SyntheticDatasetConfig, rng: np.random.Generator) -> pd.DataFrame:
    records: list[dict[str, object]] = []

    cell_index = 0

    def add_cells(n: int, state: str, branch: str, pseudotime_low: float, pseudotime_high: float) -> None:
        nonlocal cell_index
        pseudotimes = np.linspace(pseudotime_low, pseudotime_high, n)
        pseudotimes = np.clip(pseudotimes + rng.normal(0, 0.015, size=n), 0, 1)

        for pt in pseudotimes:
            cell_id = f"CELL_{cell_index:04d}"
            cell_index += 1

            if branch == "root":
                x = rng.normal(0.0, 0.25)
                y = rng.normal(0.0, 0.25)
            elif branch == "transition":
                x = 1.5 * pt + rng.normal(0.0, 0.18)
                y = rng.normal(0.0, 0.20)
            elif branch == "branch_a":
                x = 1.0 + 2.2 * pt + rng.normal(0.0, 0.20)
                y = 1.5 * pt + rng.normal(0.0, 0.20)
            elif branch == "branch_b":
                x = 1.0 + 2.2 * pt + rng.normal(0.0, 0.20)
                y = -1.5 * pt + rng.normal(0.0, 0.20)
            else:
                raise ValueError(f"Unexpected branch: {branch}")

            radius = float(np.sqrt((x - 1.5) ** 2 + y**2))
            if x < 0.8:
                spatial_domain = "left_progenitor_region"
            elif x > 2.2 and y >= 0:
                spatial_domain = "upper_terminal_region"
            elif x > 2.2 and y < 0:
                spatial_domain = "lower_terminal_region"
            elif 0.7 <= radius <= 1.3:
                spatial_domain = "transition_ring_region"
            else:
                spatial_domain = "central_transition_region"

            records.append(
                {
                    "cell_id": cell_id,
                    "true_state": state,
                    "true_branch": branch,
                    "true_pseudotime": round(float(pt), 4),
                    "spatial_x": round(float(x), 4),
                    "spatial_y": round(float(y), 4),
                    "true_spatial_domain": spatial_domain,
                }
            )

    add_cells(config.n_root_cells, "root_progenitor", "root", 0.00, 0.20)
    add_cells(config.n_transition_cells, "transition_state", "transition", 0.20, 0.55)
    add_cells(config.n_branch_a_cells, "branch_a_terminal", "branch_a", 0.50, 1.00)
    add_cells(config.n_branch_b_cells, "branch_b_terminal", "branch_b", 0.50, 1.00)

    metadata = pd.DataFrame.from_records(records)
    return metadata.sample(frac=1.0, random_state=config.random_seed).reset_index(drop=True)


def _sigmoid(x: np.ndarray, centre: float, scale: float = 12.0) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-scale * (x - centre)))


def _make_expression_matrix(
    metadata: pd.DataFrame,
    gene_names: list[str],
    rng: np.random.Generator,
) -> pd.DataFrame:
    n_cells = metadata.shape[0]
    expression = pd.DataFrame(
        rng.gamma(shape=1.2, scale=0.25, size=(n_cells, len(gene_names))),
        columns=gene_names,
    )

    pt = metadata["true_pseudotime"].to_numpy()
    branch = metadata["true_branch"].to_numpy()
    x = metadata["spatial_x"].to_numpy()
    y = metadata["spatial_y"].to_numpy()
    radius = np.sqrt((x - 1.5) ** 2 + y**2)

    root_signal = 1.5 * (1.0 - _sigmoid(pt, centre=0.28, scale=14.0))
    transition_signal = 1.8 * np.exp(-((pt - 0.48) ** 2) / 0.025)
    branch_a_signal = 2.2 * ((branch == "branch_a").astype(float)) * _sigmoid(pt, centre=0.62, scale=12.0)
    branch_b_signal = 2.2 * ((branch == "branch_b").astype(float)) * _sigmoid(pt, centre=0.62, scale=12.0)
    cycle_signal = 1.1 * (np.sin(2 * np.pi * pt * 2.2) + 1.0) / 2.0

    left_signal = 1.7 * (x < 0.8).astype(float)
    right_signal = 1.7 * (x > 2.2).astype(float)
    ring_signal = 1.8 * ((radius >= 0.7) & (radius <= 1.3)).astype(float)

    for gene in GENE_GROUPS["root_state"]:
        expression[gene] += root_signal + rng.normal(0, 0.08, size=n_cells)

    for gene in GENE_GROUPS["transition_state"]:
        expression[gene] += transition_signal + rng.normal(0, 0.08, size=n_cells)

    for gene in GENE_GROUPS["branch_a_terminal"]:
        expression[gene] += branch_a_signal + rng.normal(0, 0.08, size=n_cells)

    for gene in GENE_GROUPS["branch_b_terminal"]:
        expression[gene] += branch_b_signal + rng.normal(0, 0.08, size=n_cells)

    for gene in GENE_GROUPS["cycling"]:
        expression[gene] += cycle_signal + rng.normal(0, 0.06, size=n_cells)

    for gene in GENE_GROUPS["spatial_domain_left"]:
        expression[gene] += left_signal + rng.normal(0, 0.05, size=n_cells)

    for gene in GENE_GROUPS["spatial_domain_right"]:
        expression[gene] += right_signal + rng.normal(0, 0.05, size=n_cells)

    for gene in GENE_GROUPS["spatial_ring"]:
        expression[gene] += ring_signal + rng.normal(0, 0.05, size=n_cells)

    expression = expression.clip(lower=0.0)
    expression.insert(0, "cell_id", metadata["cell_id"].to_numpy())
    return expression.round(4)


def _make_gene_metadata(gene_names: list[str]) -> pd.DataFrame:
    rows = []
    for gene in gene_names:
        group = "noise"
        for candidate_group, genes in GENE_GROUPS.items():
            if gene in genes:
                group = candidate_group
                break

        rows.append(
            {
                "gene": gene,
                "designed_signal_group": group,
                "is_marker_gene": group != "noise",
            }
        )

    return pd.DataFrame(rows)


def generate_synthetic_dataset(
    output_dir: str | Path = "data/synthetic",
    config: SyntheticDatasetConfig | None = None,
) -> dict[str, str]:
    """Generate the controlled benchmark dataset and hidden truth files."""

    config = config or SyntheticDatasetConfig()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(config.random_seed)
    gene_names = _all_gene_names(config.n_genes)

    metadata = _make_cell_metadata(config, rng)
    expression = _make_expression_matrix(metadata, gene_names, rng)
    gene_metadata = _make_gene_metadata(gene_names)

    metadata_path = output_path / "synthetic_cell_metadata.csv"
    expression_path = output_path / "synthetic_expression_matrix.csv"
    gene_metadata_path = output_path / "synthetic_gene_metadata.csv"

    metadata.to_csv(metadata_path, index=False)
    expression.to_csv(expression_path, index=False)
    gene_metadata.to_csv(gene_metadata_path, index=False)

    hidden_truth = {
        "dataset_name": "cellfatebench_controlled_synthetic_v1",
        "random_seed": config.random_seed,
        "n_cells": int(metadata.shape[0]),
        "n_genes": int(len(gene_names)),
        "trajectory_truth": {
            "root_state": "root_progenitor",
            "transition_state": "transition_state",
            "terminal_states": ["branch_a_terminal", "branch_b_terminal"],
            "branch_labels": ["root", "transition", "branch_a", "branch_b"],
            "pseudotime_column": "true_pseudotime",
        },
        "spatial_truth": {
            "coordinate_columns": ["spatial_x", "spatial_y"],
            "domain_column": "true_spatial_domain",
            "spatially_variable_gene_groups": [
                "spatial_domain_left",
                "spatial_domain_right",
                "spatial_ring",
            ],
        },
        "topology_truth": {
            "expected_structure": "bifurcating_tree_with_transition_ring_signal",
            "expected_major_branches": 2,
            "expected_root_components": 1,
            "designed_ring_signal_genes": GENE_GROUPS["spatial_ring"],
            "interpretation_note": "The cell-state trajectory is tree-like, while spatial marker genes include a ring-pattern signal for topology-aware tasks.",
        },
        "gene_groups": GENE_GROUPS,
    }

    hidden_truth_path = output_path / "synthetic_hidden_truth.json"
    hidden_truth_path.write_text(json.dumps(hidden_truth, indent=2))

    return {
        "metadata": str(metadata_path),
        "expression": str(expression_path),
        "gene_metadata": str(gene_metadata_path),
        "hidden_truth": str(hidden_truth_path),
    }
