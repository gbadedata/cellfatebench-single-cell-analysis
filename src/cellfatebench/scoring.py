"""Scoring logic for CellFateBench solver answers."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import json

from cellfatebench.validators import (
    boolean_field_matches,
    contains_all_required_terms,
    field_value_matches,
)


TASK_ANSWER_FILES = [
    "benchmark_tasks/hidden/trajectory_pseudotime_answers.json",
    "benchmark_tasks/hidden/spatial_pattern_answers.json",
    "benchmark_tasks/hidden/topological_persistence_answers.json",
]


def load_hidden_answers(paths: list[str] | None = None) -> dict[str, dict[str, Any]]:
    """Load hidden answers keyed by task_id."""

    answer_paths = paths or TASK_ANSWER_FILES
    answers: dict[str, dict[str, Any]] = {}

    for path in answer_paths:
        records = json.loads(Path(path).read_text())
        for record in records:
            answers[record["task_id"]] = record

    return answers


def _expected_values_from_hidden_answer(hidden_answer: dict[str, Any]) -> tuple[list[str], list[str]]:
    """Extract expected answer values and likely solver answer fields."""

    mapping = [
        ("expected_root_state", ["root_state", "recovered_state", "answer"]),
        ("expected_terminal_states", ["terminal_states", "answer"]),
        ("expected_transition_state", ["early_to_late_order", "branching_interpretation", "answer"]),
        ("expected_recovered_state", ["recovered_state", "answer"]),
        ("expected_spatial_gene_groups", ["spatial_gene_groups", "answer"]),
        ("expected_domain_signals", ["domain_to_marker_signal", "answer"]),
        ("expected_recovered_domain", ["recovered_domain", "answer"]),
        ("expected_topological_interpretation", ["topological_interpretation", "answer"]),
        ("expected_recovered_topology", ["recovered_topology", "answer"]),
        ("expected_interpretation", ["correct_interpretation", "spatial_interpretation", "reason", "answer"]),
        ("expected_error_type", ["reason", "answer"]),
    ]

    expected_values: list[str] = []
    candidate_fields: list[str] = []

    for hidden_key, fields in mapping:
        if hidden_key not in hidden_answer:
            continue

        value = hidden_answer[hidden_key]
        candidate_fields.extend(fields)

        if isinstance(value, list):
            expected_values.extend(str(item) for item in value)
        elif isinstance(value, dict):
            expected_values.extend(str(item) for item in value.values())
        else:
            expected_values.append(str(value))

    return expected_values, sorted(set(candidate_fields))


def score_single_answer(
    task_id: str,
    solver_answer: dict[str, Any],
    hidden_answer: dict[str, Any],
) -> dict[str, Any]:
    """Score a single solver answer with partial credit."""

    score = 0.0
    max_score = 1.0
    checks: dict[str, Any] = {}

    expected_values, candidate_fields = _expected_values_from_hidden_answer(hidden_answer)

    label_match = False
    if expected_values:
        label_match = field_value_matches(solver_answer, candidate_fields, expected_values)
        if label_match:
            score += 0.55

    checks["label_or_claim_match"] = label_match

    boolean_match = None
    if "expected_claim_supported" in hidden_answer:
        boolean_match = boolean_field_matches(
            solver_answer,
            ["claim_supported", "is_cyclic_cell_fate_trajectory", "answer"],
            hidden_answer["expected_claim_supported"],
        )
        if boolean_match:
            score += 0.55
        checks["boolean_claim_match"] = boolean_match

    if "expected_is_cyclic_cell_fate_trajectory" in hidden_answer:
        boolean_match = boolean_field_matches(
            solver_answer,
            ["is_cyclic_cell_fate_trajectory", "claim_supported", "answer"],
            hidden_answer["expected_is_cyclic_cell_fate_trajectory"],
        )
        if boolean_match:
            score += 0.55
        checks["boolean_cyclic_match"] = boolean_match

    required_terms = hidden_answer.get("required_evidence_terms", [])
    found_terms, total_terms = contains_all_required_terms(solver_answer, required_terms)

    evidence_score = 0.0
    if total_terms > 0:
        evidence_score = 0.35 * (found_terms / total_terms)
        score += evidence_score

    checks["required_evidence_terms_found"] = found_terms
    checks["required_evidence_terms_total"] = total_terms

    confidence_present = "confidence" in solver_answer
    if confidence_present:
        score += 0.10

    checks["confidence_present"] = confidence_present

    final_score = round(min(score, max_score), 4)

    return {
        "task_id": task_id,
        "score": final_score,
        "passed": final_score >= 0.70,
        "checks": checks,
    }


def score_solver_answers(
    solver_answers_path: str | Path,
    output_path: str | Path = "results/reports/sample_solver_score_report.json",
) -> dict[str, Any]:
    """Score a set of solver answers."""

    hidden_answers = load_hidden_answers()
    solver_answers = json.loads(Path(solver_answers_path).read_text())

    task_results = []
    for answer in solver_answers:
        task_id = answer["task_id"]
        if task_id not in hidden_answers:
            task_results.append(
                {
                    "task_id": task_id,
                    "score": 0.0,
                    "passed": False,
                    "error": "task_id not found in hidden answer keys",
                }
            )
            continue

        task_results.append(score_single_answer(task_id, answer, hidden_answers[task_id]))

    total_tasks = len(task_results)
    passed_tasks = sum(1 for result in task_results if result.get("passed"))
    average_score = round(
        sum(float(result["score"]) for result in task_results) / total_tasks,
        4,
    ) if total_tasks else 0.0

    report = {
        "total_tasks_scored": total_tasks,
        "passed_tasks": passed_tasks,
        "average_score": average_score,
        "task_results": task_results,
    }

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2))

    return report
