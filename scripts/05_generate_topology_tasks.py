"""Generate CellFateBench topological-persistence benchmark tasks."""

from cellfatebench.tasks import generate_topology_tasks


def main() -> None:
    outputs = generate_topology_tasks()
    print("Generated topological-persistence benchmark assets:")
    for name, path in outputs.items():
        print(f"- {name}: {path}")


if __name__ == "__main__":
    main()
