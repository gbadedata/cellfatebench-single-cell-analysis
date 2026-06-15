"""Generate CellFateBench design-stage calibration log."""

from cellfatebench.calibration import write_calibration_log


def main() -> None:
    output = write_calibration_log()
    print("Generated design-stage calibration log:")
    print(f"- calibration_log: {output}")


if __name__ == "__main__":
    main()
