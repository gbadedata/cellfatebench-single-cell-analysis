# CellFateBench v2: Public Data and RNA Velocity Extension Plan

## Purpose

CellFateBench v1 established a controlled single-cell benchmark framework with synthetic hidden truth, public tasks, hidden answers, oracle outputs, validators, scoring, calibration logs, Docker reproducibility, GitHub Actions CI, and professional documentation.

Version 2 extends the benchmark with a public RNA velocity dataset and scVelo-style velocity reasoning tasks while preserving the clean v1 architecture.

The purpose of v2 is to add biological realism and velocity-aware reasoning without weakening the deterministic benchmark foundation created in v1.

## v2 Scope

CellFateBench v2 will add:

1. A public RNA velocity dataset preparation layer.
2. Velocity-derived summary outputs.
3. A new velocity reasoning benchmark task family.
4. Expanded scoring rubric support.
5. Solver performance summary outputs.
6. Empirical calibration and task difficulty rebalancing.
7. v2-specific documentation and evidence mapping.
8. Docker and CI validation for the extended workflow.

## Public Dataset Strategy

The v2 dataset layer will use a public RNA velocity dataset through scVelo’s supported dataset interface.

The first target dataset will be the scVelo pancreas dataset because it is commonly used in RNA velocity examples and contains the spliced and unspliced layers required for velocity analysis.

Large raw dataset files will not be committed to Git unless repository size, licensing, and reproducibility constraints are reviewed. Instead, the project will provide scripts that load the public dataset and generate lightweight derived summaries.

## Why Public Data Is Added in v2

The v1 controlled synthetic dataset was appropriate for deterministic hidden-truth benchmark design.

The v2 public dataset extension adds biological realism. It allows the project to demonstrate public data handling, AnnData validation, scVelo-style preprocessing, RNA velocity interpretation, and real-data benchmark task construction.

The project will clearly distinguish between:

* controlled synthetic hidden truth;
* public dataset reference annotations;
* velocity-derived evidence;
* benchmark scoring assumptions.

## New Benchmark Task Family

The new task family will be:

```
velocity_reasoning
```

Initial task types will include:

1. Velocity-supported root-direction inference.
2. Terminal fate support from velocity summaries.
3. Velocity contradiction detection.
4. Latent-time ordering.
5. Low-confidence velocity failure-mode interpretation.
6. Marker and velocity evidence alignment.

## Expected v2 Outputs

Planned outputs include:

```
benchmark_tasks/public/velocity_reasoning_tasks.json
benchmark_tasks/hidden/velocity_reasoning_answers.json
benchmark_tasks/oracle_outputs/velocity_reasoning_oracle_outputs.json
benchmark_tasks/calibration_logs/empirical_velocity_calibration_log.json

results/tables/velocity_dataset_summary.csv
results/tables/velocity_task_summary.csv
results/tables/solver_performance_summary.csv
results/tables/task_difficulty_rebalanced.csv

results/figures/velocity_confidence_by_state.png
results/figures/solver_score_by_task_family.png
results/figures/task_difficulty_rebalance.png
```

## Expanded Scoring Rubric

The expanded scoring rubric will support:

* answer correctness;
* evidence support;
* contradiction handling;
* uncertainty discipline;
* confidence reporting;
* overclaim penalty;
* family-specific scoring rules.

The goal is to improve evaluation quality while keeping the scoring logic transparent and testable.

## Solver Performance Outputs

Version 2 will introduce multiple sample solver profiles:

* oracle solver;
* strong sample solver;
* weak sample solver;
* overclaiming solver;
* random baseline solver.

These profiles will support empirical calibration and dashboard-ready performance summaries.

## Difficulty Rebalancing

Task difficulty will be rebalanced using solver performance evidence.

The calibration layer will identify:

* tasks that are too easy;
* tasks that are too hard;
* tasks with ambiguous evidence;
* tasks that trigger overclaiming;
* tasks requiring rewritten prompts;
* recommended difficulty changes.

## Out of Scope for v2

The following are intentionally out of scope for v2:

* full multi-omic integration;
* large-scale web dashboard deployment;
* clinical interpretation claims;
* committing large raw public datasets without review;
* claiming frontier-model calibration without actual model runs.

These may be considered for later versions.

## Quality Standard

Version 2 must preserve the quality of v1.

Every new module must have:

* clear purpose;
* tests;
* reproducible script entry point;
* documented outputs;
* Makefile command where appropriate;
* CI compatibility;
* Docker compatibility where practical;
* honest limitations.

## Completion Criteria

CellFateBench v2 will be considered complete when:

1. Public RNA velocity dataset loading is reproducible.
2. Velocity summaries are generated and saved.
3. Velocity reasoning tasks are created.
4. Hidden answers and oracle outputs are generated.
5. Expanded scoring works on sample solver profiles.
6. Solver performance summary tables and figures are generated.
7. Empirical calibration and difficulty rebalancing outputs are created.
8. Tests pass locally.
9. The v2 pipeline runs successfully.
10. Docker and CI pass.
11. README and documentation are updated.
