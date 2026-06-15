"""Tests for spatial-pattern benchmark task generation."""

import json
from pathlib import Path

from cellfatebench.tasks import generate_spatial_tasks


def test_generate_spatial_tasks(tmp_path: Path) -> None:
    outputs = generate_spatial_tasks(tmp_path)

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
    assert all(task["task_family"] == "spatial_pattern_reasoning" for task in public_tasks)


def test_spatial_public_tasks_do_not_expose_hidden_answer_keys(tmp_path: Path) -> None:
    outputs = generate_spatial_tasks(tmp_path)
    public_text = Path(outputs["public_tasks"]).read_text()

    forbidden_terms = [
        "expected_spatial_gene_groups",
        "expected_domain_signals",
        "expected_recovered_domain",
        "expected_claim_supported",
    ]

    for term in forbidden_terms:
        assert term not in public_text


def test_spatial_masked_domain_task_contains_masked_domain(tmp_path: Path) -> None:
    outputs = generate_spatial_tasks(tmp_path)
    public_tasks = json.loads(Path(outputs["public_tasks"]).read_text())

    masked_tasks = [
        task for task in public_tasks
        if task["task_id"] == "spatial_masked_domain_recovery_003"
    ]

    assert len(masked_tasks) == 1
    assert "MASKED_SPATIAL_DOMAIN" in str(masked_tasks[0])


def test_spatial_false_positive_task_exists(tmp_path: Path) -> None:
    outputs = generate_spatial_tasks(tmp_path)
    public_tasks = json.loads(Path(outputs["public_tasks"]).read_text())

    task_ids = {task["task_id"] for task in public_tasks}
    assert "spatial_false_positive_signal_detection_004" in task_ids
