"""Generate the CellFateBench controlled synthetic dataset."""

from cellfatebench.synthetic import generate_synthetic_dataset


def main() -> None:
    outputs = generate_synthetic_dataset()
    print("Generated CellFateBench synthetic dataset:")
    for name, path in outputs.items():
        print(f"- {name}: {path}")


if __name__ == "__main__":
    main()
