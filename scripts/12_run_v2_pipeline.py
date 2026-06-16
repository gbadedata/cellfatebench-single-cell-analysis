from __future__ import annotations

from cellfatebench.v2_pipeline import run_v2_pipeline, validate_v2_expected_outputs


def main() -> None:
    outputs = run_v2_pipeline()
    validation = validate_v2_expected_outputs()

    print("CellFateBench v2 public RNA velocity pipeline completed.")
    print("Pipeline sections:")

    for section in outputs:
        print(f"- {section}")

    if not all(validation.values()):
        missing = [path for path, exists in validation.items() if not exists]
        raise FileNotFoundError(
            "The v2 pipeline completed, but expected outputs are missing: "
            + ", ".join(missing)
        )

    print("All expected v2 outputs are present.")


if __name__ == "__main__":
    main()
