"""Tests for trajectory/pseudotime benchmark task generation."""

import json
from pathlib import Path

from cellfatebench.tasks import generate_trajectory_tasks


def test_generate_trajectory_tasks(tmp_path: Path) -> None:
    outputs = generate_trajectory_tasks(tmp_path)

    public_tasks = json.loads(Path(outputs["public_tasks"]).read_text())
    hidden_answers = json.loads(Path(outputs["hidden_answers"]).read_text())
    oracle_outputs = json.loads(Path(outputs["oracle_outputs"]).read_text())

    assert len(public_tasks) == 4
    assert len(hidden_answers) == 4
    assert len(oracle_outputs) == 4

    public_ids = {task["task_id"] for task in public_tasks}
    hidden_ids = {answer["task_id"] for answer in hidden_answers}
    oracle_ids = {oracle["task_id"] for oracle in oracle_outputs}

    assert public_ids == hidden_ids == oracle_ids

    assert all(task["task_family"] == "trajectory_pseudotime_reasoning" for task in public_tasks)
    assert any(task["difficulty"] == "hard" for task in public_tasks)


def test_public_tasks_do_not_expose_hidden_answer_keys(tmp_path: Path) -> None:
    outputs = generate_trajectory_tasks(tmp_path)
    public_text = Path(outputs["public_tasks"]).read_text()

    forbidden_terms = [
        "expected_root_state",
        "expected_terminal_states",
        "expected_recovered_state",
        "expected_order",
    ]

    for term in forbidden_terms:
        assert term not in public_text


def test_masked_terminal_task_contains_masked_state(tmp_path: Path) -> None:
    outputs = generate_trajectory_tasks(tmp_path)
    public_tasks = json.loads(Path(outputs["public_tasks"]).read_text())

    masked_tasks = [
        task for task in public_tasks
        if task["task_id"] == "trajectory_masked_terminal_recovery_004"
    ]

    assert len(masked_tasks) == 1
    assert "MASKED_TERMINAL_STATE" in str(masked_tasks[0])
