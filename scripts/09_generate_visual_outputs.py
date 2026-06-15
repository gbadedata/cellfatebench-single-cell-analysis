"""Generate CellFateBench visual outputs and summary tables."""

from cellfatebench.visualization import generate_all_visual_outputs


def main() -> None:
    outputs = generate_all_visual_outputs()
    print("Generated CellFateBench visual outputs:")
    for name, path in outputs.items():
        print(f"- {name}: {path}")


if __name__ == "__main__":
    main()
