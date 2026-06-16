from __future__ import annotations

from cellfatebench.velocity_solver_evaluation import write_velocity_performance_outputs


def main() -> None:
    outputs = write_velocity_performance_outputs()

    print("Velocity solver evaluation completed.")
    for name, path in outputs.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
