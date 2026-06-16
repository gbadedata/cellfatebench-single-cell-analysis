# Reviewer Guide

## Project

CellFateBench: Single-Cell Genomics Benchmark for Scientific Reasoning

Repository:

https://github.com/gbadedata/cellfatebench-single-cell-analysis

## Purpose of This Guide

This guide is written for a technical reviewer, hiring panel member, research engineer, bioinformatics lead, scientific software evaluator, or computational biology reviewer who wants to inspect CellFateBench efficiently.

CellFateBench is not just a single-cell analysis script. It is a benchmark-design project that turns single-cell genomics workflows into structured evaluation assets.

The project includes:

* controlled synthetic single-cell data with known hidden truth;
* public RNA velocity dataset summaries;
* public benchmark tasks;
* hidden answer keys;
* oracle outputs;
* scoring logic;
* solver evaluation;
* calibration logs;
* difficulty rebalancing;
* reproducible pipelines;
* Docker validation;
* GitHub Actions CI;
* reviewer-focused documentation.

## What This Project Demonstrates

CellFateBench demonstrates the ability to:

* design original benchmark tasks grounded in single-cell genomics;
* generate controlled synthetic data with known hidden truth;
* handle a public RNA velocity dataset responsibly;
* separate public prompts from hidden answer keys;
* write oracle outputs with scientific rationale;
* build validators and scoring logic;
* design partial-credit evaluation;
* penalise unsupported overclaiming;
* document task difficulty and likely failure modes;
* perform empirical sample-solver calibration;
* rebalance task difficulty using solver-performance evidence;
* use topology-aware analysis with GUDHI;
* orchestrate reproducible v1 and v2 pipelines;
* run tests locally and in CI;
* validate reproducibility with Docker;
* document evidence and limitations honestly.

## What the Project Is Not

This project is not:

* a clinical diagnostic tool;
* a regulated biomedical reporting system;
* a replacement for experimental validation;
* a large-scale biological atlas;
* a claim of empirical frontier-model calibration;
* a full scVelo velocity graph analysis pipeline;
* a production laboratory decision system.

The v2 empirical calibration is based on local sample solver profiles. It does not claim to benchmark frontier models.

## Recommended Review Path

A reviewer can inspect the project in the following order.

### 1. Start with the README

File:

* `README.md`

The README gives the high-level summary, v1 and v2 architecture, data strategy, task families, outputs, testing, Docker, CI, and limitations.

### 2. Inspect the methods

File:

* `docs/methods.md`

This explains dataset design, task design, public and hidden answer separation, scoring, calibration, reproducibility, and scope.

### 3. Inspect the evidence map

File:

* `docs/evidence_map.md`

This maps project claims to specific files, tests, generated outputs, and CI evidence.

### 4. Inspect public benchmark tasks

Files:

* `benchmark_tasks/public/trajectory_pseudotime_tasks.json`
* `benchmark_tasks/public/spatial_pattern_tasks.json`
* `benchmark_tasks/public/topological_persistence_tasks.json`
* `benchmark_tasks/public/velocity_reasoning_tasks.json`

These show the visible benchmark prompts and evidence provided to a solver.

### 5. Inspect hidden answer keys

Files:

* `benchmark_tasks/hidden/trajectory_pseudotime_answers.json`
* `benchmark_tasks/hidden/spatial_pattern_answers.json`
* `benchmark_tasks/hidden/topological_persistence_answers.json`
* `benchmark_tasks/hidden/velocity_reasoning_answers.json`

These contain expected answers and scoring-relevant evidence fields.

### 6. Inspect oracle outputs

Files:

* `benchmark_tasks/oracle_outputs/trajectory_pseudotime_oracle_outputs.json`
* `benchmark_tasks/oracle_outputs/spatial_pattern_oracle_outputs.json`
* `benchmark_tasks/oracle_outputs/topological_persistence_oracle_outputs.json`
* `benchmark_tasks/oracle_outputs/velocity_reasoning_oracle_outputs.json`

These show reference-style answers with conclusions, confidence levels, rationale, and supporting evidence.

### 7. Inspect generated result outputs

Useful review outputs include:

* `results/tables/benchmark_task_summary.csv`
* `results/tables/topology_summary.json`
* `results/tables/velocity_dataset_summary.csv`
* `results/tables/velocity_layer_summary.csv`
* `results/tables/velocity_solver_performance_summary.csv`
* `results/tables/velocity_task_performance_summary.csv`
* `results/tables/velocity_task_difficulty_rebalanced.csv`
* `results/reports/sample_solver_score_report.json`

Useful figures include:

* `results/figures/synthetic_spatial_layout.png`
* `results/figures/pseudotime_by_branch.png`
* `results/figures/task_family_counts.png`
* `results/figures/sample_solver_scores.png`
* `results/figures/velocity_solver_score_by_profile.png`
* `results/figures/velocity_task_pass_rate.png`
* `results/figures/velocity_task_difficulty_rebalance.png`

### 8. Run the tests

Command:

`make test`

Expected result:

`57 passed`

The public scVelo pancreas dataset may emit AnnData old-format warnings. These warnings come from upstream H5AD metadata conventions and do not indicate failure of CellFateBench logic.

### 9. Run the v1 pipeline

Command:

`make pipeline`

Expected result:

`CellFateBench full pipeline completed. All expected outputs are present.`

### 10. Run the v2 pipeline

Command:

`make pipeline-v2`

Expected result:

`CellFateBench v2 public RNA velocity pipeline completed. All expected v2 outputs are present.`

### 11. Run Docker validation

Commands:

* `docker build -t cellfatebench:latest .`
* `docker run --rm cellfatebench:latest make test`
* `docker run --rm cellfatebench:latest make pipeline`
* `docker run --rm cellfatebench:latest make pipeline-v2`

These commands validate that the benchmark can run in a clean container environment.

## Repository Structure

Key folders:

* `src/cellfatebench/`: Python package source code
* `scripts/`: executable workflow scripts
* `tests/`: pytest test suite
* `data/synthetic/`: generated controlled synthetic dataset
* `benchmark_tasks/public/`: public benchmark task files
* `benchmark_tasks/hidden/`: hidden answer keys
* `benchmark_tasks/oracle_outputs/`: oracle reference answers
* `benchmark_tasks/calibration_logs/`: calibration review assets
* `results/tables/`: generated summary tables
* `results/figures/`: generated visual outputs
* `results/reports/`: generated scoring reports
* `sample_solver_answers/`: sample solver answer files and velocity solver profiles
* `docs/`: project documentation

## Key Source Files

### Synthetic dataset generation

File:

* `src/cellfatebench/synthetic.py`

Purpose:

* creates controlled single-cell scenarios with known hidden truth;
* generates metadata, expression matrix, gene metadata, and hidden truth JSON.

### v1 benchmark task generation

File:

* `src/cellfatebench/tasks.py`

Purpose:

* generates public tasks, hidden answers, and oracle outputs for trajectory, spatial, and topological reasoning.

### Topology summary

File:

* `src/cellfatebench/topology.py`

Purpose:

* uses GUDHI to compute lightweight topology-aware persistence summaries;
* creates trajectory and spatial topology summaries.

### Validators

File:

* `src/cellfatebench/validators.py`

Purpose:

* provides deterministic text and field-matching utilities;
* supports scoring logic.

### v1 scoring

File:

* `src/cellfatebench/scoring.py`

Purpose:

* scores solver answers against hidden answer keys;
* supports partial credit;
* writes a score report.

### v1 calibration

File:

* `src/cellfatebench/calibration.py`

Purpose:

* generates design-stage calibration logs;
* documents difficulty, reasoning requirements, and likely failure modes.

### Public RNA velocity dataset validation

File:

* `src/cellfatebench/public_velocity.py`

Purpose:

* validates public RNA velocity dataset shape, required layers, annotation columns, and layer summaries.

### v2 velocity task generation

File:

* `src/cellfatebench/velocity_tasks.py`

Purpose:

* generates public RNA velocity reasoning tasks, hidden answers, and oracle outputs.

### v2 velocity solver evaluation

File:

* `src/cellfatebench/velocity_solver_evaluation.py`

Purpose:

* evaluates sample velocity solver profiles;
* scores correctness, evidence support, uncertainty discipline, and overclaiming.

### v2 calibration

File:

* `src/cellfatebench/velocity_calibration.py`

Purpose:

* performs empirical sample-solver calibration;
* produces difficulty rebalancing outputs.

### v1 pipeline

File:

* `src/cellfatebench/pipeline.py`

Purpose:

* orchestrates the full v1 benchmark generation pipeline.

### v2 pipeline

File:

* `src/cellfatebench/v2_pipeline.py`

Purpose:

* orchestrates the full v2 public RNA velocity extension pipeline.

### Visualization

File:

* `src/cellfatebench/visualization.py`

Purpose:

* generates figures and benchmark summary tables.

## Benchmark Task Families

### Trajectory and pseudotime reasoning

These tasks test whether a solver can infer:

* root or progenitor state;
* terminal states;
* transition placement;
* early-to-late pseudotime ordering;
* masked terminal identity.

### Spatial pattern reasoning

These tasks test whether a solver can infer:

* spatially variable genes;
* spatial-domain marker enrichment;
* masked spatial domains;
* unsupported spatial claims.

### Topological persistence reasoning

These tasks test whether a solver can infer:

* bifurcating structure;
* major branch count;
* ring-signal meaning;
* false-positive loop claims;
* difference between spatial topology and cell-fate topology.

### RNA velocity reasoning

These tasks test whether a solver can reason about:

* upstream cell-state evidence;
* terminal endocrine fate support;
* contradiction detection;
* latent-time-style ordering;
* low-confidence velocity interpretation;
* marker and velocity evidence alignment.

## How to Assess Project Quality

A reviewer should look for the following quality signals.

### Benchmark design quality

* Are public tasks separated from hidden answers?
* Are oracle outputs available for inspection?
* Are task prompts structured and reproducible?
* Are scoring fields explicit?
* Are unsupported claims penalised?

### Scientific reasoning quality

* Do tasks require evidence synthesis rather than label recall?
* Are uncertainty and overclaiming handled?
* Are topology and RNA velocity claims scoped carefully?
* Are public data annotations treated as reference context rather than absolute truth?

### Software engineering quality

* Is the project organised as a package?
* Are scripts separated from source modules?
* Are tests present and passing?
* Are outputs reproducible through Makefile commands?
* Does Docker run the same validation?
* Does GitHub Actions validate the project remotely?

### Documentation quality

* Does the README explain the project clearly?
* Does the methods document explain the scientific rationale?
* Does the evidence map link claims to files?
* Does the limitations document avoid overclaiming?

## Expected Local Validation

A strong local validation result should include:

* `make test` passing;
* `make pipeline` passing;
* `make pipeline-v2` passing;
* no unexpected untracked files;
* generated output files present;
* CI passing on GitHub.

## Main Strengths

The project is strong because it combines:

* single-cell genomics task design;
* benchmark-style public and hidden file separation;
* synthetic hidden truth for deterministic scoring;
* public RNA velocity data for biological realism;
* GUDHI-based topology summaries;
* explicit scoring and calibration;
* difficulty rebalancing;
* Docker reproducibility;
* CI validation;
* reviewer-focused documentation.

## Main Limitations to Note

The project is honest about limitations:

* synthetic data cannot capture the full complexity of real single-cell biology;
* public dataset annotations are reference context, not absolute truth;
* v2 does not yet compute a full scVelo velocity graph;
* v2 calibration is based on local sample solver profiles, not frontier-model runs;
* the project is not clinical or diagnostic.

## Suggested Review Decision

A reviewer should treat CellFateBench as a serious portfolio-grade scientific software project that demonstrates benchmark construction, computational biology reasoning, reproducibility, and documentation discipline.

It should not be reviewed as a biological discovery paper or a clinical workflow. Its value is in the benchmark-engineering framework, reproducible implementation, and evidence-aware evaluation design.
