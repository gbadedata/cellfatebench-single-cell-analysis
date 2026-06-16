from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from anndata import AnnData

from cellfatebench.public_velocity import (
    infer_annotation_column,
    layer_summary_to_frame,
    summarise_velocity_dataset,
    validate_velocity_layers,
    velocity_summary_to_frame,
    write_velocity_dataset_outputs,
)


def make_velocity_adata() -> AnnData:
    matrix = np.array(
        [
            [1.0, 0.0, 3.0],
            [0.0, 2.0, 1.0],
            [4.0, 1.0, 0.0],
            [2.0, 3.0, 1.0],
        ]
    )
    obs = pd.DataFrame(
        {"clusters": ["root", "transition", "branch_a", "branch_b"]},
        index=[f"cell_{idx}" for idx in range(matrix.shape[0])],
    )
    var = pd.DataFrame(index=[f"gene_{idx}" for idx in range(matrix.shape[1])])
    adata = AnnData(X=matrix, obs=obs, var=var)
    adata.layers["spliced"] = matrix + 1.0
    adata.layers["unspliced"] = matrix * 0.5
    return adata


def test_validate_velocity_layers_returns_layer_shapes() -> None:
    adata = make_velocity_adata()

    layer_shapes = validate_velocity_layers(adata)

    assert layer_shapes == {
        "spliced": (4, 3),
        "unspliced": (4, 3),
    }


def test_validate_velocity_layers_rejects_missing_required_layer() -> None:
    adata = make_velocity_adata()
    del adata.layers["unspliced"]

    with pytest.raises(ValueError, match="Missing required RNA velocity layer"):
        validate_velocity_layers(adata)


def test_validate_velocity_layers_rejects_shape_mismatch() -> None:
    class FakeAnnData:
        shape = (4, 3)
        layers = {
            "spliced": np.ones((2, 3)),
            "unspliced": np.ones((4, 3)),
        }

    with pytest.raises(ValueError, match="has shape"):
        validate_velocity_layers(FakeAnnData())


def test_infer_annotation_column_finds_cluster_column() -> None:
    adata = make_velocity_adata()

    assert infer_annotation_column(adata) == "clusters"


def test_summarise_velocity_dataset_returns_expected_values() -> None:
    adata = make_velocity_adata()

    summary = summarise_velocity_dataset(adata, dataset_name="unit_test_velocity")

    assert summary.dataset_name == "unit_test_velocity"
    assert summary.n_cells == 4
    assert summary.n_genes == 3
    assert summary.required_layers_present is True
    assert summary.missing_layers == ()
    assert summary.annotation_column == "clusters"
    assert summary.n_annotation_groups == 4


def test_velocity_summary_to_frame_has_expected_columns() -> None:
    adata = make_velocity_adata()
    summary = summarise_velocity_dataset(adata, dataset_name="unit_test_velocity")

    frame = velocity_summary_to_frame(summary)

    assert frame.shape[0] == 1
    assert set(frame.columns) == {
        "dataset_name",
        "n_cells",
        "n_genes",
        "required_layers_present",
        "missing_layers",
        "annotation_column",
        "n_annotation_groups",
    }


def test_layer_summary_to_frame_has_one_row_per_required_layer() -> None:
    adata = make_velocity_adata()

    frame = layer_summary_to_frame(adata)

    assert set(frame["layer"]) == {"spliced", "unspliced"}
    assert set(frame["n_cells"]) == {4}
    assert set(frame["n_genes"]) == {3}


def test_write_velocity_dataset_outputs_creates_csv_files(tmp_path) -> None:
    adata = make_velocity_adata()
    summary_path = tmp_path / "velocity_dataset_summary.csv"
    layer_path = tmp_path / "velocity_layer_summary.csv"

    returned_summary_path, returned_layer_path = write_velocity_dataset_outputs(
        adata=adata,
        dataset_name="unit_test_velocity",
        summary_output_path=summary_path,
        layer_output_path=layer_path,
    )

    assert returned_summary_path == summary_path
    assert returned_layer_path == layer_path
    assert summary_path.exists()
    assert layer_path.exists()

    summary_frame = pd.read_csv(summary_path)
    layer_frame = pd.read_csv(layer_path)

    assert summary_frame.loc[0, "dataset_name"] == "unit_test_velocity"
    assert set(layer_frame["layer"]) == {"spliced", "unspliced"}
