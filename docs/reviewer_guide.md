# Reviewer Guide

## Project

CellFateBench: A Single-Cell Benchmark for Trajectory, Spatial, and Topological Analysis

Repository:

https://github.com/gbadedata/cellfatebench-single-cell-analysis

## Purpose of This Guide

This guide is written for a technical reviewer, hiring panel member, research engineer, bioinformatics lead, or scientific software evaluator who wants to understand what the project does and how to inspect it efficiently.

CellFateBench is a benchmark-design project. It is not just a single-cell analysis script. It builds a small but complete evaluation framework around controlled single-cell genomics tasks.

## What This Project Demonstrates

CellFateBench demonstrates the ability to:

* design original benchmark tasks grounded in single-cell genomics;
* generate controlled synthetic data with known hidden truth;
* create public tasks and hidden answer keys;
* write oracle outputs with scientific rationale;
* build validators and scoring logic;
* design partial-credit evaluation;
* document task difficulty and likely failure modes;
* use topology-aware analysis with GUDHI;
* orchestrate a reproducible full pipeline;
* run tests locally and in CI;
* validate reproducibility with Docker.

## What the Project Is Not

This project is not:

* a clinical diagnostic tool;
* a regulated biomedical reporting system;
* a replacement for experimental validation;
* a large-scale biological atlas;
* a claim of empirical frontier-model calibration.

The current calibration is a design-stage calibration review. It documents expected difficulty and failure modes but does not claim that tasks have already been benchmarked against frontier models.

## Recommended Review Path

A reviewer can inspect the project in the following order.

### 1. Start With the README

File:

* `README.md`

The README gives the high-level summary, architecture, task families, outputs, testing, Docker, and CI information.

### 2. Inspect the Methods

File:

* `docs/methods.md`

This explains the dataset design, task design, scoring, calibration, reproducibility, and limitations.

### 3. Inspect the Evidence Map

File:

* `docs/evidence_map.md`

This maps project claims to specific files and outputs.

### 4. Inspect the Public Benchmark Tasks

Files:

* `benchmark_tasks/public/trajectory_pseudotime_tasks.json`
* `benchmark_tasks/public/spatial_pattern_tasks.json`
* `benchmark_tasks/public/topological_persistence_tasks.json`

These show the actual public benchmark problems.

### 5. Inspect the Hidden Answer Keys

Files:

* `benchmark_tasks/hidden/trajectory_pseudotime_answers.json`
* `benchmark_tasks/hidden/spatial_pattern_answers.json`
* `benchmark_tasks/hidden/topological_persistence_answers.json`

These contain the expected answers and scoring-relevant evidence terms.

### 6. Inspect the Oracle Outputs

Files:

* `benchmark_tasks/oracle_outputs/trajectory_pseudotime_oracle_outputs.json`
* `benchmark_tasks/oracle_outputs/spatial_pattern_oracle_outputs.json`
* `benchmark_tasks/oracle_outputs/topological_persistence_oracle_outputs.json`

These show what strong reference-style answers look like.

### 7. Run the Tests

Command:

```
make test
```

Expected result:

```
27 passed
```

### 8. Run the Full Pipeline

Command:

```
make pipeline
```

Expected result:

```
CellFateBench full pipeline completed.
All expected outputs are present.
```

### 9. Run Docker Validation

Commands:

```
docker build -t cellfatebench:latest .
docker run --rm cellfatebench:latest make test
docker run --rm cellfatebench:latest make pipeline
```

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
* `docs/`: project documentation

## Key Source Files

### Synthetic Dataset Generation

File:

* `src/cellfatebench/synthetic.py`

Purpose:

* creates controlled single-cell scenarios with known hidden truth;
* generates metadata, expression matrix, gene metadata, and hidden truth JSON.

### Benchmark Task Generation

File:

* `src/cellfatebench/tasks.py`

Purpose:

* generates public tasks, hidden answers, and oracle outputs for:

  * trajectory reasoning;
  * spatial reasoning;
  * topological reasoning.

### Topology Summary

File:

* `src/cellfatebench/topology.py`

Purpose:

* uses GUDHI to compute topology-aware persistence summaries;
* creates trajectory and spatial topology summaries.

### Validators

File:

* `src/cellfatebench/validators.py`

Purpose:

* provides deterministic text and field-matching utilities;
* supports scoring logic.

### Scoring

File:

* `src/cellfatebench/scoring.py`

Purpose:

* scores solver answers against hidden answer keys;
* supports partial credit;
* writes a score report.

### Calibration

File:

* `src/cellfatebench/calibration.py`

Purpose:

* generates design-stage calibration logs;
* documents difficulty, reasoning requirements, and likely failure modes.

### Pipeline

File:

* `src/cellfatebench/pipeline.py`

Purpose:

* orchestrates the full benchmark generation pipeline.

### Visualization

File:

* `src/cellfatebench/visualization.py`

Purpose:

* generates figures and benchmark summary tables.

## Benchmark Task Families

### Trajectory and Pseudotime Reasoning

These tasks test whether a solver can infer:

* root/progenitor state;
* terminal states;
* pseudotime ordering;
* transition-state position;
* masked terminal identity.

### Spatial Pattern Reasoning

These tasks test whether a solver can infer:

* spatially variable gene groups;
* spatial-domain marker signals;
* masked spatial domains;
* false-positive spatial claims.

### Topological Persistence Reasoning

These tasks test whether a solver can infer:

* bifurcating trajectory structure;
* major branch count;
* spatial ring signal interpretation;
* false-positive loop claims;
* distinction between spatial topology and trajectory topology.

## Why Controlled Synthetic Data Was Used

The project uses controlled synthetic data because benchmark evaluation requires known hidden truth.

For a benchmark, it is not enough to ask an interesting question. The benchmark must know the answer.

Controlled synthetic data allows the project to define:

* true branch labels;
* true terminal states;
* true pseudotime;
* true spatial domains;
* true spatially variable gene groups;
* true topology design.

This makes deterministic validation possible.

## How to Interpret the Calibration Log

File:

* `benchmark_tasks/calibration_logs/design_stage_calibration_log.json`

The calibration log should be read as a design-stage review. It documents:

* what each task is testing;
* why the task has its declared difficulty;
* where solvers are likely to fail;
* what future calibration should test.

It is not an empirical model-calibration result.

## Main Strengths

The project is strong because it combines:

* single-cell genomics task design;
* benchmark engineering;
* hidden-answer separation;
* oracle outputs;
* scoring and validation;
* calibration review;
* topology-aware analysis;
* Docker reproducibility;
* CI validation;
* professional documentation.

## Main Limitations

The project also has clear limitations:

* the first version uses synthetic data;
* the calibration is design-stage, not empirical frontier-model calibration;
* the benchmark does not yet include scVelo or Squidpy workflows;
* the dataset is intentionally compact to keep CI and Docker reproducibility practical;
* the project is not intended for clinical or diagnostic use.

## Suggested Future Improvements

Future versions could add:

* empirical calibration against multiple AI systems;
* human expert calibration;
* real public single-cell datasets;
* scVelo-style RNA velocity tasks;
* Squidpy-style spatial-neighbourhood tasks;
* multi-omic integration tasks;
* richer topological summaries and persistence diagrams;
* task difficulty rebalancing based on solver performance.

## Reviewer Conclusion

CellFateBench should be reviewed as a scientific software and benchmark-design project.

Its strongest contribution is not simply that it runs a single-cell workflow. Its strongest contribution is that it converts controlled single-cell analysis scenarios into public benchmark tasks, hidden answers, oracle outputs, validators, scoring reports, calibration logs, and reproducible evidence.

This makes the project closely aligned with computational scientific software, bioinformatics benchmark design, and single-cell genomics reasoning evaluation.
