from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd


REQUIRED_VELOCITY_LAYERS = ("spliced", "unspliced")
DEFAULT_ANNOTATION_CANDIDATES = (
    "clusters",
    "celltype",
    "cell_type",
    "annotation",
    "cell_annotation",
)


@dataclass(frozen=True)
class VelocityDatasetSummary:
    """Structured summary for a public RNA velocity AnnData object."""

    dataset_name: str
    n_cells: int
    n_genes: int
    required_layers_present: bool
    missing_layers: tuple[str, ...]
    annotation_column: str | None
    n_annotation_groups: int | None


def _shape_of_layer(layer: Any) -> tuple[int, int]:
    """Return a safe 2D shape tuple for an AnnData layer-like object."""
    shape = getattr(layer, "shape", None)
    if shape is None or len(shape) != 2:
        raise ValueError("Velocity layer does not expose a valid two-dimensional shape.")
    return int(shape[0]), int(shape[1])


def validate_velocity_layers(
    adata: Any,
    required_layers: tuple[str, ...] = REQUIRED_VELOCITY_LAYERS,
) -> dict[str, tuple[int, int]]:
    """
    Validate that an AnnData-like object contains required RNA velocity layers.

    RNA velocity workflows require layer-level count matrices such as spliced
    and unspliced counts. This function checks for those layers and validates
    that their shapes match the main AnnData matrix shape.
    """
    if not hasattr(adata, "layers"):
        raise TypeError("Expected an AnnData-like object with a .layers attribute.")

    if not hasattr(adata, "shape"):
        raise TypeError("Expected an AnnData-like object with a .shape attribute.")

    expected_shape = tuple(int(value) for value in adata.shape)
    missing_layers = [layer for layer in required_layers if layer not in adata.layers]

    if missing_layers:
        missing = ", ".join(missing_layers)
        raise ValueError(f"Missing required RNA velocity layer(s): {missing}")

    layer_shapes: dict[str, tuple[int, int]] = {}

    for layer_name in required_layers:
        layer_shape = _shape_of_layer(adata.layers[layer_name])
        if layer_shape != expected_shape:
            raise ValueError(
                f"Layer '{layer_name}' has shape {layer_shape}, "
                f"but AnnData matrix has shape {expected_shape}."
            )
        layer_shapes[layer_name] = layer_shape

    return layer_shapes


def infer_annotation_column(
    adata: Any,
    candidates: tuple[str, ...] = DEFAULT_ANNOTATION_CANDIDATES,
) -> str | None:
    """Infer a likely cell annotation column from AnnData.obs."""
    if not hasattr(adata, "obs"):
        return None

    obs_columns = set(str(column) for column in adata.obs.columns)

    for column in candidates:
        if column in obs_columns:
            return column

    return None


def summarise_velocity_dataset(
    adata: Any,
    dataset_name: str,
    annotation_candidates: tuple[str, ...] = DEFAULT_ANNOTATION_CANDIDATES,
) -> VelocityDatasetSummary:
    """Create a high-level summary for a public RNA velocity dataset."""
    layer_shapes = validate_velocity_layers(adata)
    missing_layers = tuple(
        layer for layer in REQUIRED_VELOCITY_LAYERS if layer not in layer_shapes
    )

    annotation_column = infer_annotation_column(adata, annotation_candidates)

    n_annotation_groups: int | None = None
    if annotation_column is not None:
        n_annotation_groups = int(adata.obs[annotation_column].astype(str).nunique())

    return VelocityDatasetSummary(
        dataset_name=dataset_name,
        n_cells=int(adata.n_obs),
        n_genes=int(adata.n_vars),
        required_layers_present=len(missing_layers) == 0,
        missing_layers=missing_layers,
        annotation_column=annotation_column,
        n_annotation_groups=n_annotation_groups,
    )


def velocity_summary_to_frame(summary: VelocityDatasetSummary) -> pd.DataFrame:
    """Convert a velocity dataset summary into a one-row table."""
    return pd.DataFrame(
        [
            {
                "dataset_name": summary.dataset_name,
                "n_cells": summary.n_cells,
                "n_genes": summary.n_genes,
                "required_layers_present": summary.required_layers_present,
                "missing_layers": ";".join(summary.missing_layers),
                "annotation_column": summary.annotation_column,
                "n_annotation_groups": summary.n_annotation_groups,
            }
        ]
    )


def layer_summary_to_frame(
    adata: Any,
    required_layers: tuple[str, ...] = REQUIRED_VELOCITY_LAYERS,
) -> pd.DataFrame:
    """Create a layer-level summary table for RNA velocity inputs."""
    layer_shapes = validate_velocity_layers(adata, required_layers=required_layers)

    records = []
    for layer_name, shape in layer_shapes.items():
        layer = adata.layers[layer_name]
        records.append(
            {
                "layer": layer_name,
                "n_cells": shape[0],
                "n_genes": shape[1],
                "matrix_type": type(layer).__name__,
            }
        )

    return pd.DataFrame(records)


def write_velocity_dataset_outputs(
    adata: Any,
    dataset_name: str,
    summary_output_path: Path,
    layer_output_path: Path,
) -> tuple[Path, Path]:
    """Write dataset-level and layer-level velocity summary outputs."""
    summary = summarise_velocity_dataset(adata, dataset_name=dataset_name)
    summary_frame = velocity_summary_to_frame(summary)
    layer_frame = layer_summary_to_frame(adata)

    summary_output_path.parent.mkdir(parents=True, exist_ok=True)
    layer_output_path.parent.mkdir(parents=True, exist_ok=True)

    summary_frame.to_csv(summary_output_path, index=False)
    layer_frame.to_csv(layer_output_path, index=False)

    return summary_output_path, layer_output_path
