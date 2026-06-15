"""Run the full CellFateBench benchmark pipeline."""

from cellfatebench.pipeline import run_full_pipeline, validate_expected_outputs


def main() -> None:
    outputs = run_full_pipeline()
    validation = validate_expected_outputs()

    print("CellFateBench full pipeline completed.")
    print("Pipeline sections:")
    for name in outputs:
        print(f"- {name}")

    missing = [path for path, exists in validation.items() if not exists]

    if missing:
        print("Missing expected outputs:")
        for path in missing:
            print(f"- {path}")
        raise SystemExit(1)

    print("All expected outputs are present.")


if __name__ == "__main__":
    main()
