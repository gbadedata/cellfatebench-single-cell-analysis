"""Generate CellFateBench spatial-pattern benchmark tasks."""

from cellfatebench.tasks import generate_spatial_tasks


def main() -> None:
    outputs = generate_spatial_tasks()
    print("Generated spatial-pattern benchmark assets:")
    for name, path in outputs.items():
        print(f"- {name}: {path}")


if __name__ == "__main__":
    main()
