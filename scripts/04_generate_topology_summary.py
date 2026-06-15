"""Generate topology-aware CellFateBench summary outputs."""

from cellfatebench.topology import write_topology_summary


def main() -> None:
    output = write_topology_summary()
    print("Generated topology summary:")
    print(f"- topology_summary: {output}")


if __name__ == "__main__":
    main()
