from __future__ import annotations

import json
from pathlib import Path
from typing import Any


VELOCITY_TASK_FAMILY = "velocity_reasoning"

PANCREAS_CLUSTER_COUNTS = {
    "Alpha": 481,
    "Beta": 591,
    "Delta": 70,
    "Ductal": 916,
    "Epsilon": 142,
    "Ngn3 high EP": 642,
    "Ngn3 low EP": 262,
    "Pre-endocrine": 592,
}

REFERENCE_ENDOCRINE_ORDERING = [
    "Ductal",
    "Ngn3 low EP",
    "Ngn3 high EP",
    "Pre-endocrine",
    "Alpha/Beta/Delta/Epsilon",
]


def build_velocity_public_tasks() -> list[dict[str, Any]]:
    """Build public velocity reasoning benchmark tasks."""
    shared_dataset_context = {
        "dataset_name": "scvelo_pancreas",
        "n_cells": 3696,
        "n_genes": 27998,
        "annotation_column": "clusters",
        "cluster_counts": PANCREAS_CLUSTER_COUNTS,
        "available_layers": ["spliced", "unspliced"],
        "available_embeddings": ["X_pca", "X_umap"],
        "important_scope_note": (
            "These tasks use public scVelo pancreas metadata and RNA velocity layer "
            "availability. Full velocity graph computation is introduced in a later v2 step."
        ),
    }

    return [
        {
            "task_id": "velocity_root_direction_inference_001",
            "task_family": VELOCITY_TASK_FAMILY,
            "difficulty": "medium",
            "task_type": "velocity_supported_root_direction_inference",
            "prompt": (
                "Using the public scVelo pancreas cluster structure and RNA velocity layer "
                "availability, identify the most plausible early upstream cell population "
                "for an endocrine differentiation interpretation. Explain the evidence "
                "that supports your answer."
            ),
            "observable_evidence": {
                **shared_dataset_context,
                "candidate_states": [
                    "Ductal",
                    "Ngn3 low EP",
                    "Ngn3 high EP",
                    "Pre-endocrine",
                    "Alpha",
                    "Beta",
                    "Delta",
                    "Epsilon",
                ],
                "reference_progression_hint": (
                    "Endocrine differentiation tasks should distinguish upstream ductal or "
                    "endocrine progenitor-like populations from terminal endocrine states."
                ),
            },
            "expected_response_format": {
                "answer": "string",
                "supporting_evidence": "list of strings",
                "confidence": "float between 0 and 1",
            },
        },
        {
            "task_id": "velocity_terminal_fate_support_002",
            "task_family": VELOCITY_TASK_FAMILY,
            "difficulty": "medium",
            "task_type": "terminal_fate_support_from_velocity_context",
            "prompt": (
                "Identify the terminal endocrine fate groups represented in the public "
                "pancreas cluster labels. Explain why these should be treated as terminal "
                "fate candidates rather than early progenitor states."
            ),
            "observable_evidence": {
                **shared_dataset_context,
                "candidate_terminal_labels": ["Alpha", "Beta", "Delta", "Epsilon"],
                "candidate_non_terminal_labels": [
                    "Ductal",
                    "Ngn3 low EP",
                    "Ngn3 high EP",
                    "Pre-endocrine",
                ],
            },
            "expected_response_format": {
                "answer": "list of strings",
                "supporting_evidence": "list of strings",
                "confidence": "float between 0 and 1",
            },
        },
        {
            "task_id": "velocity_contradiction_detection_003",
            "task_family": VELOCITY_TASK_FAMILY,
            "difficulty": "hard",
            "task_type": "velocity_contradiction_detection",
            "prompt": (
                "A solver claims that the most plausible endocrine differentiation direction "
                "is from Alpha, Beta, Delta, and Epsilon cells back into Ductal cells. "
                "Decide whether this claim should be accepted or rejected, and justify your "
                "decision using the dataset context."
            ),
            "observable_evidence": {
                **shared_dataset_context,
                "claim_to_evaluate": (
                    "Terminal endocrine cell types are upstream of ductal cells in the "
                    "differentiation interpretation."
                ),
                "reference_ordering_hint": REFERENCE_ENDOCRINE_ORDERING,
            },
            "expected_response_format": {
                "accept_claim": "boolean",
                "supporting_evidence": "list of strings",
                "confidence": "float between 0 and 1",
            },
        },
        {
            "task_id": "velocity_latent_time_ordering_004",
            "task_family": VELOCITY_TASK_FAMILY,
            "difficulty": "hard",
            "task_type": "latent_time_ordering_reasoning",
            "prompt": (
                "Propose a biologically plausible early-to-late ordering of the annotated "
                "pancreas populations for a velocity-aware endocrine differentiation task. "
                "The answer should distinguish progenitor-like, transitional, and terminal "
                "states."
            ),
            "observable_evidence": {
                **shared_dataset_context,
                "available_cluster_labels": list(PANCREAS_CLUSTER_COUNTS.keys()),
                "ordering_instruction": (
                    "Use cluster identity and endocrine differentiation context. Do not claim "
                    "that a full latent-time computation has already been performed."
                ),
            },
            "expected_response_format": {
                "ordered_groups": "list of strings",
                "supporting_evidence": "list of strings",
                "confidence": "float between 0 and 1",
            },
        },
        {
            "task_id": "velocity_low_confidence_failure_mode_005",
            "task_family": VELOCITY_TASK_FAMILY,
            "difficulty": "hard",
            "task_type": "uncertainty_and_failure_mode_detection",
            "prompt": (
                "A solver sees that spliced and unspliced layers exist and immediately claims "
                "a precise velocity direction for every cluster without computing moments, "
                "velocities, or velocity confidence. Should this answer be treated as fully "
                "supported? Explain the failure mode."
            ),
            "observable_evidence": {
                **shared_dataset_context,
                "claim_to_evaluate": (
                    "Layer availability alone is sufficient to make precise per-cluster "
                    "velocity direction claims."
                ),
                "available_evidence": [
                    "spliced layer exists",
                    "unspliced layer exists",
                    "cluster annotations exist",
                    "full velocity graph and confidence summaries are not yet included in this task",
                ],
            },
            "expected_response_format": {
                "accept_claim": "boolean",
                "failure_mode": "string",
                "supporting_evidence": "list of strings",
                "confidence": "float between 0 and 1",
            },
        },
        {
            "task_id": "velocity_marker_velocity_alignment_006",
            "task_family": VELOCITY_TASK_FAMILY,
            "difficulty": "hard",
            "task_type": "marker_velocity_alignment_reasoning",
            "prompt": (
                "Explain how a future solver should evaluate whether marker-gene evidence "
                "and RNA velocity evidence support the same endocrine transition. The answer "
                "should describe what agreement and disagreement would look like."
            ),
            "observable_evidence": {
                **shared_dataset_context,
                "reasoning_targets": [
                    "marker evidence",
                    "spliced and unspliced layers",
                    "velocity direction",
                    "transition state interpretation",
                    "terminal fate interpretation",
                ],
                "scope_boundary": (
                    "This task evaluates reasoning design. It should not invent uncomputed "
                    "gene-level velocity values."
                ),
            },
            "expected_response_format": {
                "answer": "string",
                "agreement_criteria": "list of strings",
                "disagreement_criteria": "list of strings",
                "confidence": "float between 0 and 1",
            },
        },
    ]


def build_velocity_hidden_answers() -> list[dict[str, Any]]:
    """Build hidden answer keys for velocity reasoning benchmark tasks."""
    return [
        {
            "task_id": "velocity_root_direction_inference_001",
            "expected_answer": "Ductal",
            "accepted_answers": ["Ductal", "Ductal or endocrine progenitor-like upstream population"],
            "required_evidence_terms": ["Ductal", "upstream", "progenitor", "terminal"],
            "confidence_guidance": "Moderate confidence because full velocity graph computation is not yet included.",
        },
        {
            "task_id": "velocity_terminal_fate_support_002",
            "expected_answer": ["Alpha", "Beta", "Delta", "Epsilon"],
            "accepted_answers": [["Alpha", "Beta", "Delta", "Epsilon"]],
            "required_evidence_terms": ["terminal", "endocrine", "Alpha", "Beta"],
            "confidence_guidance": "High confidence for identifying terminal fate labels from annotation context.",
        },
        {
            "task_id": "velocity_contradiction_detection_003",
            "expected_boolean_claim": False,
            "expected_answer": "Reject the claim",
            "required_evidence_terms": ["reject", "terminal", "Ductal", "upstream"],
            "confidence_guidance": "High confidence because the proposed direction reverses the expected interpretation.",
        },
        {
            "task_id": "velocity_latent_time_ordering_004",
            "expected_answer": REFERENCE_ENDOCRINE_ORDERING,
            "accepted_answers": [
                [
                    "Ductal",
                    "Ngn3 low EP",
                    "Ngn3 high EP",
                    "Pre-endocrine",
                    "Alpha/Beta/Delta/Epsilon",
                ]
            ],
            "required_evidence_terms": ["Ductal", "Ngn3", "Pre-endocrine", "terminal"],
            "confidence_guidance": "Moderate confidence because this is a reference ordering, not a computed latent-time result.",
        },
        {
            "task_id": "velocity_low_confidence_failure_mode_005",
            "expected_boolean_claim": False,
            "expected_answer": "Layer availability alone is insufficient for precise velocity direction claims.",
            "required_evidence_terms": ["spliced", "unspliced", "insufficient", "confidence"],
            "confidence_guidance": "High confidence because the task explicitly withholds computed velocity confidence summaries.",
        },
        {
            "task_id": "velocity_marker_velocity_alignment_006",
            "expected_answer": "Marker and velocity evidence should be checked for directional agreement without inventing uncomputed values.",
            "required_evidence_terms": ["marker", "velocity", "agreement", "disagreement", "direction"],
            "confidence_guidance": "Moderate confidence because this is a reasoning-design task.",
        },
    ]


def build_velocity_oracle_outputs() -> list[dict[str, Any]]:
    """Build oracle-style outputs for velocity reasoning tasks."""
    return [
        {
            "task_id": "velocity_root_direction_inference_001",
            "oracle_answer": "Ductal",
            "rationale": (
                "Ductal is the most plausible upstream population in this public pancreas "
                "velocity context because the terminal endocrine labels are Alpha, Beta, "
                "Delta, and Epsilon, while Ngn3 and pre-endocrine labels represent "
                "intermediate endocrine differentiation states."
            ),
            "evidence_terms": ["Ductal", "upstream", "Ngn3", "terminal endocrine states"],
            "confidence": 0.72,
        },
        {
            "task_id": "velocity_terminal_fate_support_002",
            "oracle_answer": ["Alpha", "Beta", "Delta", "Epsilon"],
            "rationale": (
                "Alpha, Beta, Delta, and Epsilon correspond to endocrine fate labels. "
                "They should be treated as terminal fate candidates rather than early "
                "progenitor-like states."
            ),
            "evidence_terms": ["Alpha", "Beta", "Delta", "Epsilon", "terminal"],
            "confidence": 0.86,
        },
        {
            "task_id": "velocity_contradiction_detection_003",
            "oracle_answer": {"accept_claim": False},
            "rationale": (
                "The claim should be rejected because it reverses the expected direction. "
                "Terminal endocrine labels should not be treated as upstream of Ductal "
                "in this differentiation interpretation."
            ),
            "evidence_terms": ["reject", "terminal", "Ductal", "upstream"],
            "confidence": 0.88,
        },
        {
            "task_id": "velocity_latent_time_ordering_004",
            "oracle_answer": REFERENCE_ENDOCRINE_ORDERING,
            "rationale": (
                "A plausible reference ordering is Ductal, Ngn3 low EP, Ngn3 high EP, "
                "Pre-endocrine, then the terminal endocrine fates. This should be described "
                "as a reference ordering unless latent time has been explicitly computed."
            ),
            "evidence_terms": ["Ductal", "Ngn3 low EP", "Ngn3 high EP", "Pre-endocrine", "terminal"],
            "confidence": 0.74,
        },
        {
            "task_id": "velocity_low_confidence_failure_mode_005",
            "oracle_answer": {"accept_claim": False},
            "rationale": (
                "The claim should not be treated as fully supported. Spliced and unspliced "
                "layers are required inputs for RNA velocity, but layer availability alone "
                "does not prove precise velocity direction for every cluster."
            ),
            "evidence_terms": ["spliced", "unspliced", "insufficient", "velocity confidence"],
            "confidence": 0.9,
        },
        {
            "task_id": "velocity_marker_velocity_alignment_006",
            "oracle_answer": (
                "Marker and velocity evidence should be evaluated for directional agreement "
                "without inventing uncomputed gene-level velocity values."
            ),
            "rationale": (
                "A future solver should compare marker-defined state transitions with "
                "computed velocity direction and confidence. Agreement means marker evidence, "
                "transition-state identity, and velocity direction support the same biological "
                "progression. Disagreement means marker interpretation and velocity direction "
                "point to different transitions or the velocity confidence is too weak."
            ),
            "evidence_terms": ["marker", "velocity", "agreement", "disagreement", "direction"],
            "confidence": 0.78,
        },
    ]


def write_velocity_task_files(
    public_output_path: Path = Path("benchmark_tasks/public/velocity_reasoning_tasks.json"),
    hidden_output_path: Path = Path("benchmark_tasks/hidden/velocity_reasoning_answers.json"),
    oracle_output_path: Path = Path("benchmark_tasks/oracle_outputs/velocity_reasoning_oracle_outputs.json"),
) -> tuple[Path, Path, Path]:
    """Write velocity public tasks, hidden answers, and oracle outputs."""
    public_tasks = build_velocity_public_tasks()
    hidden_answers = build_velocity_hidden_answers()
    oracle_outputs = build_velocity_oracle_outputs()

    for path, payload in [
        (public_output_path, public_tasks),
        (hidden_output_path, hidden_answers),
        (oracle_output_path, oracle_outputs),
    ]:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    return public_output_path, hidden_output_path, oracle_output_path
