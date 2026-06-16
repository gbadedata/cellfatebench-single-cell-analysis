from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

from cellfatebench.public_velocity import write_velocity_dataset_outputs


DEFAULT_CONFIG_PATH = Path("configs/velocity_public_dataset.yml")


def load_velocity_config(config_path: Path = DEFAULT_CONFIG_PATH) -> dict[str, Any]:
    """Load the public velocity dataset configuration file."""
    if not config_path.exists():
        raise FileNotFoundError(f"Velocity dataset config not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle)

    if not isinstance(config, dict) or "dataset" not in config:
        raise ValueError("Velocity config must contain a top-level 'dataset' section.")

    return config


def load_scvelo_pancreas_dataset() -> Any:
    """
    Load the public scVelo pancreas dataset.

    The dataset is accessed through scVelo's dataset interface. Large raw data
    files are not committed to this repository. This function may download or
    read cached data depending on the local scVelo setup.
    """
    try:
        import scvelo as scv
    except ImportError as exc:
        raise ImportError(
            "scvelo is required for the public RNA velocity extension. "
            "Install the project environment from environment.yml."
        ) from exc

    return scv.datasets.pancreas()


def prepare_public_velocity_dataset(
    config_path: Path = DEFAULT_CONFIG_PATH,
) -> tuple[Path, Path]:
    """Load, validate, and summarise the configured public RNA velocity dataset."""
    config = load_velocity_config(config_path)
    dataset_config = config["dataset"]

    dataset_name = str(dataset_config["name"])
    outputs = dataset_config["outputs"]

    summary_output_path = Path(outputs["dataset_summary"])
    layer_output_path = Path(outputs["layer_summary"])

    if dataset_name != "scvelo_pancreas":
        raise ValueError(
            f"Unsupported public velocity dataset '{dataset_name}'. "
            "The current v2 implementation supports 'scvelo_pancreas'."
        )

    adata = load_scvelo_pancreas_dataset()

    return write_velocity_dataset_outputs(
        adata=adata,
        dataset_name=dataset_name,
        summary_output_path=summary_output_path,
        layer_output_path=layer_output_path,
    )


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(
        description="Prepare lightweight summaries for the public RNA velocity dataset."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help="Path to the velocity public dataset config file.",
    )
    return parser


def main() -> None:
    """Command-line entry point."""
    parser = build_parser()
    args = parser.parse_args()

    summary_path, layer_path = prepare_public_velocity_dataset(config_path=args.config)

    print("Public RNA velocity dataset preparation completed.")
    print(f"Dataset summary: {summary_path}")
    print(f"Layer summary: {layer_path}")


if __name__ == "__main__":
    main()
