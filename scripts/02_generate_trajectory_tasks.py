"""Generate CellFateBench trajectory and pseudotime benchmark tasks."""

from cellfatebench.tasks import generate_trajectory_tasks


def main() -> None:
    outputs = generate_trajectory_tasks()
    print("Generated trajectory/pseudotime benchmark assets:")
    for name, path in outputs.items():
        print(f"- {name}: {path}")


if __name__ == "__main__":
    main()
