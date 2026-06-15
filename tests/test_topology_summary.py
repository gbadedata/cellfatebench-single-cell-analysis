"""Tests for topology-aware summaries."""

import json
from pathlib import Path

from cellfatebench.topology import build_topology_summary, write_topology_summary


def test_build_topology_summary_contains_expected_sections() -> None:
    summary = build_topology_summary()

    assert "trajectory_proxy" in summary
    assert "spatial_coordinate_cloud" in summary
    assert "designed_topological_features" in summary

    assert summary["designed_topological_features"]["major_branches"] == 2
    assert summary["designed_topological_features"]["root_components"] == 1
    assert summary["designed_topological_features"]["ring_signal_genes"] == ["RING1", "RING2", "RING3"]


def test_topology_summary_persistence_fields_exist() -> None:
    summary = build_topology_summary()

    trajectory_persistence = summary["trajectory_proxy"]["persistence_summary"]
    spatial_persistence = summary["spatial_coordinate_cloud"]["persistence_summary"]

    for persistence_summary in [trajectory_persistence, spatial_persistence]:
        assert "h0_feature_count" in persistence_summary
        assert "h1_feature_count" in persistence_summary
        assert "top_h0_persistence" in persistence_summary
        assert "top_h1_persistence" in persistence_summary
        assert persistence_summary["n_points_used"] <= 300


def test_write_topology_summary(tmp_path: Path) -> None:
    output = write_topology_summary(tmp_path / "topology_summary.json")
    summary = json.loads(Path(output).read_text())

    assert summary["designed_topological_features"]["major_branches"] == 2
