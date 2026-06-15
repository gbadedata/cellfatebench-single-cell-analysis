"""Score sample CellFateBench solver answers."""

from cellfatebench.scoring import score_solver_answers


def main() -> None:
    report = score_solver_answers("sample_solver_answers/sample_answers.json")
    print("Scored sample solver answers:")
    print(f"- total_tasks_scored: {report['total_tasks_scored']}")
    print(f"- passed_tasks: {report['passed_tasks']}")
    print(f"- average_score: {report['average_score']}")
    print("- output: results/reports/sample_solver_score_report.json")


if __name__ == "__main__":
    main()
