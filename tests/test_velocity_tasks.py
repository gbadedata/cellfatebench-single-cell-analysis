from __future__ import annotations

import json

from cellfatebench.velocity_tasks import (
    VELOCITY_TASK_FAMILY,
    build_velocity_hidden_answers,
    build_velocity_oracle_outputs,
    build_velocity_public_tasks,
    write_velocity_task_files,
)


def test_velocity_public_tasks_have_expected_count_and_family() -> None:
    tasks = build_velocity_public_tasks()

    assert len(tasks) == 6
    assert {task["task_family"] for task in tasks} == {VELOCITY_TASK_FAMILY}


def test_velocity_task_ids_are_unique_across_public_hidden_and_oracle() -> None:
    public_tasks = build_velocity_public_tasks()
    hidden_answers = build_velocity_hidden_answers()
    oracle_outputs = build_velocity_oracle_outputs()

    public_ids = {task["task_id"] for task in public_tasks}
    hidden_ids = {answer["task_id"] for answer in hidden_answers}
    oracle_ids = {oracle["task_id"] for oracle in oracle_outputs}

    assert len(public_ids) == 6
    assert public_ids == hidden_ids == oracle_ids


def test_public_velocity_tasks_do_not_expose_hidden_answer_fields() -> None:
    hidden_keys = {
        "expected_answer",
        "accepted_answers",
        "expected_boolean_claim",
        "required_evidence_terms",
        "oracle_answer",
    }

    for task in build_velocity_public_tasks():
        assert hidden_keys.isdisjoint(task.keys())
        assert hidden_keys.isdisjoint(task["observable_evidence"].keys())


def test_velocity_tasks_use_real_public_pancreas_cluster_labels() -> None:
    tasks = build_velocity_public_tasks()
    first_task_evidence = tasks[0]["observable_evidence"]

    assert first_task_evidence["dataset_name"] == "scvelo_pancreas"
    assert first_task_evidence["n_cells"] == 3696
    assert first_task_evidence["n_genes"] == 27998
    assert first_task_evidence["cluster_counts"]["Ductal"] == 916
    assert first_task_evidence["cluster_counts"]["Ngn3 high EP"] == 642
    assert first_task_evidence["cluster_counts"]["Beta"] == 591


def test_velocity_hidden_answers_include_uncertainty_guidance() -> None:
    hidden_answers = build_velocity_hidden_answers()

    assert all("confidence_guidance" in answer for answer in hidden_answers)


def test_velocity_oracle_outputs_include_rationale_and_confidence() -> None:
    oracle_outputs = build_velocity_oracle_outputs()

    for oracle in oracle_outputs:
        assert "rationale" in oracle
        assert "confidence" in oracle
        assert 0 <= oracle["confidence"] <= 1


def test_write_velocity_task_files_creates_json_outputs(tmp_path) -> None:
    public_path = tmp_path / "public.json"
    hidden_path = tmp_path / "hidden.json"
    oracle_path = tmp_path / "oracle.json"

    returned_paths = write_velocity_task_files(
        public_output_path=public_path,
        hidden_output_path=hidden_path,
        oracle_output_path=oracle_path,
    )

    assert returned_paths == (public_path, hidden_path, oracle_path)
    assert public_path.exists()
    assert hidden_path.exists()
    assert oracle_path.exists()

    public_payload = json.loads(public_path.read_text())
    hidden_payload = json.loads(hidden_path.read_text())
    oracle_payload = json.loads(oracle_path.read_text())

    assert len(public_payload) == 6
    assert len(hidden_payload) == 6
    assert len(oracle_payload) == 6
