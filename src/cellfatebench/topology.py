"""Topology-aware summaries for CellFateBench.

This module uses GUDHI to compute lightweight persistent-homology summaries from
the controlled synthetic single-cell benchmark data.

The goal is not to build a full topological data analysis library. The goal is
to create deterministic topology-aware features that can support benchmark tasks
around connected structure, branching, loop-like spatial signals, and
persistence-based reasoning.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import json

import gudhi as gd
import numpy as np
import pandas as pd


def load_metadata(metadata_path: str | Path = "data/synthetic/synthetic_cell_metadata.csv") -> pd.DataFrame:
    """Load synthetic cell metadata."""

    return pd.read_csv(metadata_path)


def _sample_points(points: np.ndarray, max_points: int = 300, seed: int = 42) -> np.ndarray:
    """Deterministically sample points to keep Rips persistence computation fast."""

    if points.shape[0] <= max_points:
        return points

    rng = np.random.default_rng(seed)
    idx = rng.choice(points.shape[0], size=max_points, replace=False)
    return points[idx]


def compute_rips_persistence_summary(
    points: np.ndarray,
    max_edge_length: float = 1.5,
    max_dimension: int = 2,
    max_points: int = 300,
) -> dict[str, Any]:
    """Compute a compact Rips persistence summary using GUDHI."""

    sampled = _sample_points(points, max_points=max_points)

    rips = gd.RipsComplex(points=sampled, max_edge_length=max_edge_length)
    simplex_tree = rips.create_simplex_tree(max_dimension=max_dimension)
    persistence = simplex_tree.persistence()

    h0_persistence: list[float] = []
    h1_persistence: list[float] = []

    for dimension, interval in persistence:
        birth, death = interval
        if np.isinf(death):
            continue

        lifespan = float(death - birth)
        if dimension == 0:
            h0_persistence.append(lifespan)
        elif dimension == 1:
            h1_persistence.append(lifespan)

    h0_persistence = sorted(h0_persistence, reverse=True)
    h1_persistence = sorted(h1_persistence, reverse=True)

    return {
        "n_points_used": int(sampled.shape[0]),
        "h0_feature_count": int(len(h0_persistence)),
        "h1_feature_count": int(len(h1_persistence)),
        "top_h0_persistence": [round(x, 4) for x in h0_persistence[:10]],
        "top_h1_persistence": [round(x, 4) for x in h1_persistence[:10]],
        "max_h0_persistence": round(float(max(h0_persistence)) if h0_persistence else 0.0, 4),
        "max_h1_persistence": round(float(max(h1_persistence)) if h1_persistence else 0.0, 4),
    }


def build_topology_summary(
    metadata_path: str | Path = "data/synthetic/synthetic_cell_metadata.csv",
    hidden_truth_path: str | Path = "data/synthetic/synthetic_hidden_truth.json",
) -> dict[str, Any]:
    """Build topology-aware summaries from spatial coordinates and branch metadata."""

    metadata = load_metadata(metadata_path)
    hidden_truth = json.loads(Path(hidden_truth_path).read_text())

    spatial_points = metadata[["spatial_x", "spatial_y"]].to_numpy()

    # A simple trajectory proxy: pseudotime and signed branch coordinate.
    branch_map = {
        "root": 0.0,
        "transition": 0.0,
        "branch_a": 1.0,
        "branch_b": -1.0,
    }
    trajectory_points = np.column_stack(
        [
            metadata["true_pseudotime"].to_numpy(),
            metadata["true_branch"].map(branch_map).to_numpy(),
        ]
    )

    spatial_persistence = compute_rips_persistence_summary(
        spatial_points,
        max_edge_length=1.2,
        max_dimension=2,
        max_points=300,
    )
    trajectory_persistence = compute_rips_persistence_summary(
        trajectory_points,
        max_edge_length=0.45,
        max_dimension=2,
        max_points=300,
    )

    branch_counts = metadata["true_branch"].value_counts().to_dict()
    state_counts = metadata["true_state"].value_counts().to_dict()

    summary = {
        "dataset_name": hidden_truth["dataset_name"],
        "topology_truth_note": hidden_truth["topology_truth"],
        "branch_count_summary": {str(k): int(v) for k, v in branch_counts.items()},
        "state_count_summary": {str(k): int(v) for k, v in state_counts.items()},
        "trajectory_proxy": {
            "description": "2D proxy using true pseudotime and signed branch coordinate",
            "expected_interpretation": "bifurcating trajectory with two terminal branches",
            "persistence_summary": trajectory_persistence,
        },
        "spatial_coordinate_cloud": {
            "description": "2D spatial coordinate cloud with designed left, terminal, and ring-like spatial signals",
            "expected_interpretation": "spatial layout contains a transition-ring signal while cell-state trajectory remains bifurcating",
            "persistence_summary": spatial_persistence,
        },
        "designed_topological_features": {
            "major_branches": hidden_truth["topology_truth"]["expected_major_branches"],
            "root_components": hidden_truth["topology_truth"]["expected_root_components"],
            "ring_signal_genes": hidden_truth["topology_truth"]["designed_ring_signal_genes"],
        },
    }

    return summary


def write_topology_summary(
    output_path: str | Path = "results/tables/topology_summary.json",
) -> str:
    """Write topology summary to disk."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    summary = build_topology_summary()
    output_path.write_text(json.dumps(summary, indent=2))

    return str(output_path)
