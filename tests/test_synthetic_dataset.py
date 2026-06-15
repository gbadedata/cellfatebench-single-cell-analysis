"""Tests for controlled synthetic dataset generation."""

import json
from pathlib import Path

import pandas as pd

from cellfatebench.synthetic import generate_synthetic_dataset


def test_synthetic_dataset_generation(tmp_path: Path) -> None:
    outputs = generate_synthetic_dataset(tmp_path)

    metadata = pd.read_csv(outputs["metadata"])
    expression = pd.read_csv(outputs["expression"])
    gene_metadata = pd.read_csv(outputs["gene_metadata"])
    hidden_truth = json.loads(Path(outputs["hidden_truth"]).read_text())

    assert metadata.shape[0] == 900
    assert expression.shape[0] == 900
    assert expression.shape[1] == 61
    assert gene_metadata.shape[0] == 60

    assert metadata["true_branch"].nunique() == 4
    assert set(hidden_truth["trajectory_truth"]["terminal_states"]) == {
        "branch_a_terminal",
        "branch_b_terminal",
    }

    assert "spatial_x" in metadata.columns
    assert "spatial_y" in metadata.columns
    assert "true_spatial_domain" in metadata.columns

    marker_genes = gene_metadata[gene_metadata["is_marker_gene"]]
    assert marker_genes.shape[0] > 20


def test_hidden_truth_contains_topology_and_spatial_design(tmp_path: Path) -> None:
    outputs = generate_synthetic_dataset(tmp_path)
    hidden_truth = json.loads(Path(outputs["hidden_truth"]).read_text())

    assert hidden_truth["topology_truth"]["expected_major_branches"] == 2
    assert "spatial_ring" in hidden_truth["gene_groups"]
    assert len(hidden_truth["gene_groups"]["spatial_ring"]) == 3
