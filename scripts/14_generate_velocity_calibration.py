from __future__ import annotations

from cellfatebench.velocity_calibration import write_velocity_calibration_outputs


def main() -> None:
    outputs = write_velocity_calibration_outputs()

    print("Velocity empirical calibration completed.")
    for name, path in outputs.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
