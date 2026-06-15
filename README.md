# CellFateBench: A Single-Cell Benchmark for Trajectory, Spatial, and Topological Analysis

![CI](https://github.com/gbadedata/cellfatebench-single-cell-analysis/actions/workflows/ci.yml/badge.svg)

CellFateBench is a scientific software and benchmark-design project for evaluating reasoning over single-cell genomics workflows.

The project creates controlled single-cell benchmark scenarios with known hidden truth, then converts those scenarios into structured reasoning tasks across trajectory analysis, spatial gene-pattern interpretation, and topology-aware analysis. It includes public task files, hidden answer keys, oracle outputs, deterministic validators, partial-credit scoring, calibration logs, visual outputs, Docker reproducibility, GitHub Actions CI, and reviewer-focused documentation.

Repository:

https://github.com/gbadedata/cellfatebench-single-cell-analysis

## Executive Summary

Many single-cell projects stop at analysis outputs such as clusters, plots, marker tables, or annotations. CellFateBench goes further by turning single-cell analysis scenarios into an evaluable benchmark.

The benchmark asks questions such as:

* Can a solver infer the root state from pseudotime and marker evidence?
* Can a solver recover a masked terminal branch?
* Can a solver identify spatially variable gene groups?
* Can a solver reject an unsupported spatial interpretation?
* Can a solver distinguish spatial ring evidence from a cyclic cell-fate trajectory?
* Can a solver reason from topology-inspired summaries without overclaiming?

The project is designed to demonstrate the skills needed for computational scientific software and evaluation design in bioinformatics and single-cell genomics.

## Scope Notice

CellFateBench is a research, learning, and portfolio project.

It is not intended for:

* clinical diagnosis;
* regulated biomedical reporting;
* production laboratory use;
* replacement of expert biological interpretation;
* replacement of experimental validation.

The current dataset is controlled and synthetic by design. This allows the benchmark to define known hidden truth for deterministic evaluation. Future versions can add public real-world single-cell datasets after the benchmark framework is established.

## Why This Project Matters

Single-cell genomics is not only about running software. It also requires interpretation.

A workflow can generate embeddings, clusters, marker tables, spatial summaries, and topology-derived outputs, but those outputs still need careful reasoning. A solver must decide what evidence supports an interpretation and what evidence should be rejected.

CellFateBench focuses on that reasoning layer.

Instead of only producing analysis outputs, the project produces a benchmark system with:

* public tasks;
* hidden answer keys;
* oracle reference outputs;
* deterministic validators;
* scoring logic;
* calibration review;
* reproducible pipeline execution;
* evidence-backed documentation.

This makes the project closer to scientific evaluation engineering than a standard exploratory analysis notebook.

## Core Capabilities Demonstrated

CellFateBench demonstrates:

* single-cell genomics benchmark design;
* controlled synthetic dataset generation;
* hidden-truth dataset construction;
* trajectory and pseudotime reasoning;
* spatial gene-pattern reasoning;
* topology-aware reasoning with GUDHI;
* public task and hidden answer separation;
* oracle output generation;
* deterministic validation;
* partial-credit scoring;
* design-stage calibration review;
* full pipeline orchestration;
* Docker reproducibility;
* GitHub Actions CI;
* technical documentation and evidence mapping.

## Project Architecture

```
Controlled synthetic single-cell dataset
        |
        v
Known hidden truth
        |
        v
Trajectory, spatial, and topology summaries
        |
        v
Public benchmark task generation
        |
        v
Hidden answer keys and oracle outputs
        |
        v
Validators and partial-credit scoring
        |
        v
Calibration logs and failure-mode review
        |
        v
Reports, summary tables, and visual outputs
        |
        v
Docker and GitHub Actions CI validation
```

## Repository Structure

```
cellfatebench-single-cell-analysis/
├── benchmark_tasks/
│   ├── public/
│   ├── hidden/
│   ├── oracle_outputs/
│   └── calibration_logs/
├── configs/
├── data/
│   ├── raw/
│   ├── processed/
│   ├── reference/
│   └── synthetic/
├── docs/
│   ├── evidence/
│   ├── evidence_map.md
│   ├── limitations.md
│   ├── methods.md
│   ├── project_design.md
│   └── reviewer_guide.md
├── results/
│   ├── figures/
│   ├── reports/
│   └── tables/
├── sample_solver_answers/
├── scripts/
├── src/cellfatebench/
├── tests/
├── Dockerfile
├── Makefile
├── environment.yml
└── README.md
```

## Dataset Design

CellFateBench uses a controlled synthetic single-cell dataset.

The first version contains:

| Dataset Feature         | Value |
| ----------------------- | ----: |
| Synthetic cells         |   900 |
| Genes                   |    60 |
| Designed branch labels  |     4 |
| Spatial domains         |     5 |
| Terminal states         |     2 |
| Benchmark task families |     3 |
| Public benchmark tasks  |    12 |
| Hidden answer keys      |    12 |
| Oracle outputs          |    12 |
| Passing tests           |    27 |

The synthetic dataset includes known hidden truth for:

* root/progenitor state;
* transition state;
* terminal branch states;
* branch labels;
* pseudotime values;
* spatial coordinates;
* spatial domains;
* spatially variable gene groups;
* topological design.

## Why Controlled Synthetic Data Was Used

Benchmark design requires known answers.

For real single-cell datasets, the true branch structure, spatial domains, or biological topology may be uncertain, partially validated, or dependent on external biological interpretation. That uncertainty is scientifically normal, but it makes deterministic benchmark scoring difficult.

Controlled synthetic data allows the benchmark to define hidden truth and evaluate solver answers in a transparent way.

This does not mean synthetic data is biologically complete. It means it is appropriate for the first version of an evaluable benchmark framework.

## Designed Gene Programmes

The dataset contains designed gene programmes for:

* root/progenitor state;
* transition state;
* branch A terminal state;
* branch B terminal state;
* cycling-like signal;
* left spatial domain;
* right spatial domain;
* ring-like spatial domain.

These programmes allow benchmark tasks to test whether a solver can use marker evidence, pseudotime summaries, spatial structure, and topology-inspired information correctly.

## Benchmark Task Families

CellFateBench currently includes three benchmark task families.

## 1. Trajectory and Pseudotime Reasoning

Files:

* `benchmark_tasks/public/trajectory_pseudotime_tasks.json`
* `benchmark_tasks/hidden/trajectory_pseudotime_answers.json`
* `benchmark_tasks/oracle_outputs/trajectory_pseudotime_oracle_outputs.json`

This family evaluates whether a solver can infer:

* the root/progenitor state;
* terminal states;
* early-to-late pseudotime ordering;
* transition-state placement;
* masked terminal-state identity.

Example reasoning challenge:

```
Given state-level pseudotime summaries and marker evidence, identify the most likely root state and justify the answer.
```

This task family tests whether a solver can combine marker evidence with pseudotime evidence instead of guessing from labels alone.

## 2. Spatial Pattern Reasoning

Files:

* `benchmark_tasks/public/spatial_pattern_tasks.json`
* `benchmark_tasks/hidden/spatial_pattern_answers.json`
* `benchmark_tasks/oracle_outputs/spatial_pattern_oracle_outputs.json`

This family evaluates whether a solver can infer:

* spatially variable gene groups;
* domain-specific marker enrichment;
* masked spatial domains;
* unsupported spatial claims.

Example reasoning challenge:

```
A spatial domain label has been masked. Recover the most likely hidden domain identity using coordinate summaries and enriched genes.
```

This task family tests whether a solver can distinguish true spatial-domain signals from unrelated expression programmes.

## 3. Topological Persistence Reasoning

Files:

* `benchmark_tasks/public/topological_persistence_tasks.json`
* `benchmark_tasks/hidden/topological_persistence_answers.json`
* `benchmark_tasks/oracle_outputs/topological_persistence_oracle_outputs.json`

This family evaluates whether a solver can reason about:

* bifurcating trajectory structure;
* major branch count;
* ring-like spatial evidence;
* false-positive loop interpretations;
* distinction between spatial topology and cell-fate trajectory topology.

The project uses GUDHI to compute lightweight persistent-homology summaries from coordinate-derived point clouds.

Example reasoning challenge:

```
A solver observes a ring-associated signal. Determine whether it represents a cyclic cell-fate trajectory or a spatial marker-pattern feature.
```

This task family tests topology-aware reasoning and helps prevent superficial interpretation of ring-like evidence.

## Public Tasks, Hidden Answers, and Oracle Outputs

The benchmark is structured around three asset types.

| Asset Type     | Purpose                                                                |
| -------------- | ---------------------------------------------------------------------- |
| Public tasks   | Visible problem statements and observable evidence                     |
| Hidden answers | Expected answers, required evidence terms, and scoring-relevant fields |
| Oracle outputs | Reference-style answers with rationale and supporting evidence         |

This separation prevents answer leakage and supports benchmark-style evaluation.

Public task files are stored in:

```
benchmark_tasks/public/
```

Hidden answer files are stored in:

```
benchmark_tasks/hidden/
```

Oracle output files are stored in:

```
benchmark_tasks/oracle_outputs/
```

## Validators and Scoring

Validation and scoring are implemented in:

* `src/cellfatebench/validators.py`
* `src/cellfatebench/scoring.py`

The scoring engine supports partial credit for:

* expected label or claim matching;
* Boolean claim correctness;
* required evidence-term coverage;
* confidence field presence.

Sample solver answers are stored in:

```
sample_solver_answers/sample_answers.json
```

The sample score report is stored in:

```
results/reports/sample_solver_score_report.json
```

The sample solver report verifies that the scoring system works end to end.

## Calibration Layer

Calibration utilities are implemented in:

* `src/cellfatebench/calibration.py`

Calibration output:

* `benchmark_tasks/calibration_logs/design_stage_calibration_log.json`

The calibration log documents:

* task family;
* declared difficulty;
* reasoning requirements;
* likely solver failure modes;
* calibration recommendations;
* empirical calibration status.

The project is explicit that this is design-stage calibration. It does not claim empirical frontier-model calibration.

Future versions can run the benchmark against multiple AI systems or human solvers and update the difficulty labels based on observed performance.

## Topology-Aware Analysis

Topology utilities are implemented in:

* `src/cellfatebench/topology.py`

Generated topology summary:

* `results/tables/topology_summary.json`

The topology layer uses GUDHI to compute Rips persistence summaries from coordinate-derived point clouds.

The purpose is not to build a full topological data analysis library. The purpose is to support benchmark tasks where a solver must reason about:

* branch structure;
* persistent features;
* spatial ring signals;
* false-positive topology claims;
* distinction between trajectory topology and spatial topology.

## Visual Outputs

Reviewer-friendly visual outputs are generated by:

* `src/cellfatebench/visualization.py`
* `scripts/09_generate_visual_outputs.py`

Generated figures:

* `results/figures/synthetic_spatial_layout.png`
* `results/figures/pseudotime_by_branch.png`
* `results/figures/task_family_counts.png`
* `results/figures/sample_solver_scores.png`

Generated summary table:

* `results/tables/benchmark_task_summary.csv`

## Example Figures

### Synthetic Spatial Layout

![Synthetic spatial layout](results/figures/synthetic_spatial_layout.png)

### Pseudotime by Branch

![Pseudotime by branch](results/figures/pseudotime_by_branch.png)

### Task Family Counts

![Task family counts](results/figures/task_family_counts.png)

### Sample Solver Scores

![Sample solver scores](results/figures/sample_solver_scores.png)

## Full Pipeline

The full benchmark pipeline is orchestrated by:

* `src/cellfatebench/pipeline.py`
* `scripts/08_run_full_pipeline.py`
* `Makefile`

Run the full pipeline with:

```
make pipeline
```

The pipeline regenerates:

* synthetic dataset;
* trajectory benchmark tasks;
* spatial benchmark tasks;
* topology summary;
* topological benchmark tasks;
* calibration log;
* sample solver score report.

Expected output:

```
CellFateBench full pipeline completed.
All expected outputs are present.
```

## Testing

Run the test suite with:

```
make test
```

Current local result:

```
27 passed
```

The test suite covers:

* synthetic dataset generation;
* trajectory task generation;
* spatial task generation;
* topology summary generation;
* topology task generation;
* scoring;
* calibration;
* full pipeline orchestration;
* visual outputs.

## Docker Reproducibility

Build the Docker image:

```
docker build -t cellfatebench:latest .
```

Run tests inside Docker:

```
docker run --rm cellfatebench:latest make test
```

Run the full pipeline inside Docker:

```
docker run --rm cellfatebench:latest make pipeline
```

Docker validation confirms that the project can run in a clean containerized environment.

## GitHub Actions CI

GitHub Actions workflow:

* `.github/workflows/ci.yml`

The CI workflow runs:

* environment setup;
* test suite;
* full benchmark pipeline;
* expected output validation;
* Docker build;
* Docker test;
* Docker pipeline execution.

This provides external validation that the project works outside the local machine.

## Quickstart

Clone the repository:

```
git clone https://github.com/gbadedata/cellfatebench-single-cell-analysis.git
cd cellfatebench-single-cell-analysis
```

Create the environment:

```
conda env create -f environment.yml
conda activate cellfatebench
```

Run tests:

```
make test
```

Run the full benchmark pipeline:

```
make pipeline
```

Generate visual outputs:

```
PYTHONPATH=src python scripts/09_generate_visual_outputs.py
```

Score sample solver answers:

```
PYTHONPATH=src python scripts/06_score_sample_solver_answers.py
```

## Main Commands

| Command                 | Purpose                              |
| ----------------------- | ------------------------------------ |
| `make test`             | Run the test suite                   |
| `make dataset`          | Generate synthetic dataset           |
| `make trajectory`       | Generate trajectory benchmark tasks  |
| `make spatial`          | Generate spatial benchmark tasks     |
| `make topology-summary` | Generate topology summary            |
| `make topology-tasks`   | Generate topological benchmark tasks |
| `make calibration`      | Generate calibration log             |
| `make score`            | Score sample solver answers          |
| `make pipeline`         | Run the full benchmark pipeline      |

## Documentation

Additional documentation:

* `docs/methods.md`
* `docs/evidence_map.md`
* `docs/reviewer_guide.md`
* `docs/limitations.md`
* `docs/project_design.md`

Recommended reviewer path:

1. Read this README.
2. Read `docs/methods.md`.
3. Inspect `docs/evidence_map.md`.
4. Inspect public tasks in `benchmark_tasks/public/`.
5. Inspect hidden answers in `benchmark_tasks/hidden/`.
6. Inspect oracle outputs in `benchmark_tasks/oracle_outputs/`.
7. Run `make test`.
8. Run `make pipeline`.
9. Run Docker validation.

## Alignment With Computational Scientific Software and Evaluation Design

This project is relevant to roles involving:

* bioinformatics benchmark design;
* single-cell genomics;
* scientific software engineering;
* AI reasoning evaluation;
* task design;
* oracle function design;
* solution validation;
* calibration review;
* computational reproducibility;
* Linux-based scientific workflows;
* containerized execution.

The project demonstrates the ability to convert scientific workflows into structured, testable, and reproducible evaluation tasks.

## Current Limitations

The project intentionally documents its limitations.

* The first version uses controlled synthetic data.
* The calibration is design-stage, not empirical frontier-model calibration.
* The current implementation does not yet include scVelo, Squidpy, or multi-omic integration tasks.
* The topology layer is lightweight and benchmark-oriented.
* The dataset is compact to keep local, Docker, and CI execution practical.
* The project is not intended for clinical or diagnostic use.

## Future Work

Future versions could add:

* empirical calibration against multiple AI systems;
* human expert calibration;
* public real-world single-cell datasets;
* scVelo-style RNA velocity tasks;
* Squidpy-style spatial-neighbourhood tasks;
* multi-omic integration tasks;
* richer persistence diagrams and topology visualisations;
* solver performance dashboards;
* difficulty rebalancing based on calibration results;
* expanded benchmark task families.

## Project Outcome

CellFateBench is a complete benchmark-design prototype for single-cell genomics reasoning.

It demonstrates how controlled single-cell scenarios can be transformed into evaluable benchmark tasks with hidden answers, oracle outputs, validators, scoring, calibration review, reproducible execution, Docker support, CI validation, and technical documentation.

The project is designed to be inspectable, reproducible, and defensible.
