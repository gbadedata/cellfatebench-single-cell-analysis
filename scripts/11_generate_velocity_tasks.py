from __future__ import annotations

from cellfatebench.velocity_tasks import write_velocity_task_files


def main() -> None:
    public_path, hidden_path, oracle_path = write_velocity_task_files()

    print("Velocity reasoning benchmark tasks generated.")
    print(f"Public tasks: {public_path}")
    print(f"Hidden answers: {hidden_path}")
    print(f"Oracle outputs: {oracle_path}")


if __name__ == "__main__":
    main()
