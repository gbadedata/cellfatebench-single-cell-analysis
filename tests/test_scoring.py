"""Tests for CellFateBench scoring."""

from pathlib import Path
import json

from cellfatebench.scoring import load_hidden_answers, score_single_answer, score_solver_answers


def test_load_hidden_answers_contains_all_task_families() -> None:
    answers = load_hidden_answers()

    assert len(answers) == 12
    assert "trajectory_root_state_inference_001" in answers
    assert "spatial_variable_gene_identification_001" in answers
    assert "topology_bifurcation_structure_inference_001" in answers


def test_score_single_answer_passes_good_root_answer() -> None:
    answers = load_hidden_answers()
    hidden = answers["trajectory_root_state_inference_001"]

    solver_answer = {
        "root_state": "root_progenitor",
        "supporting_evidence": ["lowest pseudotime", "ROOT marker enrichment", "early state"],
        "confidence": "high",
    }

    result = score_single_answer("trajectory_root_state_inference_001", solver_answer, hidden)

    assert result["passed"] is True
    assert result["score"] >= 0.70


def test_score_single_answer_fails_wrong_answer() -> None:
    answers = load_hidden_answers()
    hidden = answers["trajectory_root_state_inference_001"]

    solver_answer = {
        "root_state": "branch_a_terminal",
        "supporting_evidence": ["late terminal marker"],
        "confidence": "low",
    }

    result = score_single_answer("trajectory_root_state_inference_001", solver_answer, hidden)

    assert result["passed"] is False


def test_score_solver_answers_writes_report(tmp_path: Path) -> None:
    sample_answers = [
        {
            "task_id": "topology_bifurcation_structure_inference_001",
            "topological_interpretation": "bifurcating",
            "major_branch_count": 2,
            "supporting_evidence": ["branch_a", "branch_b", "two terminal", "bifurcating"],
            "confidence": "high",
        }
    ]

    sample_path = tmp_path / "answers.json"
    output_path = tmp_path / "report.json"

    sample_path.write_text(json.dumps(sample_answers))

    report = score_solver_answers(sample_path, output_path)

    assert output_path.exists()
    assert report["total_tasks_scored"] == 1
    assert report["passed_tasks"] == 1
