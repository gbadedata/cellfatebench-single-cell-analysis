# Evidence Map

## Project

CellFateBench: Single-Cell Genomics Benchmark for Scientific Reasoning

Repository:

https://github.com/gbadedata/cellfatebench-single-cell-analysis

## Purpose of This Evidence Map

This document maps major CellFateBench claims to the files, outputs, tests, and workflow evidence that support them.

CellFateBench is designed as a scientific benchmark-engineering project for evaluating reasoning over single-cell genomics workflows.

It includes:

* controlled synthetic benchmark data;
* public RNA velocity dataset summaries;
* public benchmark tasks;
* hidden answer keys;
* oracle outputs;
* deterministic validators;
* scoring logic;
* solver evaluation outputs;
* calibration logs;
* difficulty rebalancing outputs;
* Docker reproducibility;
* GitHub Actions CI;
* reviewer-ready documentation.

## Evidence Summary

| Claim                                                                     | Evidence                                                                                                                |
| ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| The project includes a controlled synthetic single-cell benchmark dataset | `src/cellfatebench/synthetic.py`, `scripts/01_generate_synthetic_dataset.py`, `data/synthetic/`                         |
| The synthetic dataset contains known hidden truth                         | `data/synthetic/synthetic_hidden_truth.json`                                                                            |
| The benchmark includes trajectory and pseudotime reasoning tasks          | `benchmark_tasks/public/trajectory_pseudotime_tasks.json`                                                               |
| The benchmark includes spatial-pattern reasoning tasks                    | `benchmark_tasks/public/spatial_pattern_tasks.json`                                                                     |
| The benchmark includes topology-aware reasoning tasks                     | `benchmark_tasks/public/topological_persistence_tasks.json`                                                             |
| The benchmark includes public RNA velocity reasoning tasks                | `benchmark_tasks/public/velocity_reasoning_tasks.json`                                                                  |
| Public tasks are separated from hidden answers                            | `benchmark_tasks/public/`, `benchmark_tasks/hidden/`                                                                    |
| The benchmark includes oracle outputs                                     | `benchmark_tasks/oracle_outputs/`                                                                                       |
| The project includes GUDHI-based topology summaries                       | `src/cellfatebench/topology.py`, `results/tables/topology_summary.json`                                                 |
| The project includes public RNA velocity dataset validation               | `src/cellfatebench/public_velocity.py`, `scripts/10_prepare_public_velocity_dataset.py`                                 |
| The project validates spliced and unspliced velocity layers               | `results/tables/velocity_layer_summary.csv`, `tests/test_public_velocity.py`                                            |
| The project includes velocity task generation                             | `src/cellfatebench/velocity_tasks.py`, `scripts/11_generate_velocity_tasks.py`                                          |
| The project includes validators and v1 scoring                            | `src/cellfatebench/validators.py`, `src/cellfatebench/scoring.py`                                                       |
| The project includes v2 velocity solver evaluation                        | `src/cellfatebench/velocity_solver_evaluation.py`, `scripts/13_evaluate_velocity_solvers.py`                            |
| The project includes design-stage v1 calibration                          | `src/cellfatebench/calibration.py`, `benchmark_tasks/calibration_logs/design_stage_calibration_log.json`                |
| The project includes empirical v2 sample-solver calibration               | `src/cellfatebench/velocity_calibration.py`, `benchmark_tasks/calibration_logs/empirical_velocity_calibration_log.json` |
| The project includes velocity difficulty rebalancing                      | `results/tables/velocity_task_difficulty_rebalanced.csv`, `results/figures/velocity_task_difficulty_rebalance.png`      |
| The v1 pipeline is reproducible                                           | `src/cellfatebench/pipeline.py`, `scripts/08_run_full_pipeline.py`, `Makefile`                                          |
| The v2 pipeline is reproducible                                           | `src/cellfatebench/v2_pipeline.py`, `scripts/12_run_v2_pipeline.py`, `Makefile`                                         |
| The project includes visual review outputs                                | `src/cellfatebench/visualization.py`, `results/figures/`                                                                |
| The project is tested                                                     | `tests/`, local `pytest`, GitHub Actions CI                                                                             |
| The project supports Docker reproducibility                               | `Dockerfile`, `.dockerignore`                                                                                           |
| The project runs in GitHub Actions CI                                     | `.github/workflows/ci.yml`                                                                                              |

## v1 Synthetic Dataset Evidence

The controlled synthetic dataset is generated by:

* `src/cellfatebench/synthetic.py`
* `scripts/01_generate_synthetic_dataset.py`

Generated outputs:

* `data/synthetic/synthetic_cell_metadata.csv`
* `data/synthetic/synthetic_expression_matrix.csv`
* `data/synthetic/synthetic_gene_metadata.csv`
* `data/synthetic/synthetic_hidden_truth.json`

The synthetic dataset contains:

* 900 synthetic cells;
* 60 genes;
* known root or progenitor state;
* known transition state;
* two known terminal branches;
* known pseudotime values;
* known spatial coordinates;
* known spatial domains;
* known spatially variable gene groups;
* known topological design.

This controlled design supports deterministic hidden-answer evaluation.

## v1 Benchmark Task Evidence

### 1. Trajectory and pseudotime reasoning

Public tasks:

* `benchmark_tasks/public/trajectory_pseudotime_tasks.json`

Hidden answers:

* `benchmark_tasks/hidden/trajectory_pseudotime_answers.json`

Oracle outputs:

* `benchmark_tasks/oracle_outputs/trajectory_pseudotime_oracle_outputs.json`

Task coverage:

* root-state inference;
* terminal-state inference;
* early-to-late pseudotime ordering;
* transition-state placement;
* masked terminal-state recovery.

### 2. Spatial pattern reasoning

Public tasks:

* `benchmark_tasks/public/spatial_pattern_tasks.json`

Hidden answers:

* `benchmark_tasks/hidden/spatial_pattern_answers.json`

Oracle outputs:

* `benchmark_tasks/oracle_outputs/spatial_pattern_oracle_outputs.json`

Task coverage:

* spatially variable gene identification;
* spatial-domain marker matching;
* masked spatial-domain recovery;
* false-positive spatial interpretation detection.

### 3. Topological persistence reasoning

Public tasks:

* `benchmark_tasks/public/topological_persistence_tasks.json`

Hidden answers:

* `benchmark_tasks/hidden/topological_persistence_answers.json`

Oracle outputs:

* `benchmark_tasks/oracle_outputs/topological_persistence_oracle_outputs.json`

Task coverage:

* bifurcation structure inference;
* ring-signal disambiguation;
* masked topology recovery;
* false-positive loop interpretation detection.

## v2 Public RNA Velocity Evidence

The v2 public dataset layer is implemented in:

* `src/cellfatebench/public_velocity.py`
* `scripts/10_prepare_public_velocity_dataset.py`

Generated outputs:

* `results/tables/velocity_dataset_summary.csv`
* `results/tables/velocity_layer_summary.csv`

Current public dataset summary:

| Dataset         | Cells |  Genes | Required layers    | Annotation column | Annotation groups |
| --------------- | ----: | -----: | ------------------ | ----------------- | ----------------: |
| scvelo_pancreas | 3,696 | 27,998 | spliced, unspliced | clusters          |                 8 |

The repository commits lightweight derived outputs rather than large raw public data files.

## v2 Velocity Task Evidence

Velocity task generation is implemented in:

* `src/cellfatebench/velocity_tasks.py`
* `scripts/11_generate_velocity_tasks.py`

Public tasks:

* `benchmark_tasks/public/velocity_reasoning_tasks.json`

Hidden answers:

* `benchmark_tasks/hidden/velocity_reasoning_answers.json`

Oracle outputs:

* `benchmark_tasks/oracle_outputs/velocity_reasoning_oracle_outputs.json`

Task coverage:

* root-direction inference;
* terminal fate support;
* contradiction detection;
* latent-time-style ordering;
* low-confidence failure mode detection;
* marker and velocity evidence alignment.

Relevant tests:

* `tests/test_velocity_tasks.py`

## Hidden Answer Separation Evidence

Public benchmark tasks are stored separately from hidden answer keys.

Public directory:

* `benchmark_tasks/public/`

Hidden answer directory:

* `benchmark_tasks/hidden/`

Oracle output directory:

* `benchmark_tasks/oracle_outputs/`

This separation reduces answer leakage and supports benchmark-style evaluation.

Relevant tests include:

* `tests/test_trajectory_tasks.py`
* `tests/test_spatial_tasks.py`
* `tests/test_topology_tasks.py`
* `tests/test_velocity_tasks.py`

## Topology Evidence

Topology-aware summaries are generated by:

* `src/cellfatebench/topology.py`
* `scripts/04_generate_topology_summary.py`

Output:

* `results/tables/topology_summary.json`

The topology layer uses GUDHI to compute lightweight Rips persistence summaries from coordinate-derived point clouds.

The topology tasks evaluate whether a solver can distinguish:

* bifurcating cell-state structure;
* spatial ring-pattern evidence;
* unsupported loop claims;
* confusion between spatial topology and cell-fate trajectory topology.

## v1 Scoring Evidence

Scoring and validation logic is implemented in:

* `src/cellfatebench/validators.py`
* `src/cellfatebench/scoring.py`

Sample solver answers:

* `sample_solver_answers/sample_answers.json`

Sample score report:

* `results/reports/sample_solver_score_report.json`

The scoring framework supports partial credit for:

* expected label or claim matching;
* Boolean claim correctness;
* required evidence-term coverage;
* confidence field presence.

Relevant tests:

* `tests/test_scoring.py`

## v2 Velocity Solver Evaluation Evidence

Velocity solver evaluation is implemented in:

* `src/cellfatebench/velocity_solver_evaluation.py`
* `scripts/13_evaluate_velocity_solvers.py`

Sample velocity solver profiles:

* `sample_solver_answers/velocity_solver_profiles.json`

Generated outputs:

* `results/tables/velocity_solver_performance_summary.csv`
* `results/tables/velocity_task_performance_summary.csv`
* `results/figures/velocity_solver_score_by_profile.png`
* `results/figures/velocity_task_pass_rate.png`

The v2 scoring framework evaluates:

* correctness;
* evidence support;
* uncertainty discipline;
* no-overclaim discipline;
* unsupported precision claims.

Relevant tests:

* `tests/test_velocity_solver_evaluation.py`

## Calibration Evidence

### v1 design-stage calibration

Calibration utilities are implemented in:

* `src/cellfatebench/calibration.py`

Calibration output:

* `benchmark_tasks/calibration_logs/design_stage_calibration_log.json`

This log documents:

* declared task difficulty;
* task family;
* reasoning requirements;
* likely solver failure modes;
* calibration recommendations;
* empirical calibration status.

### v2 empirical sample-solver calibration

Velocity calibration is implemented in:

* `src/cellfatebench/velocity_calibration.py`
* `scripts/14_generate_velocity_calibration.py`

Generated outputs:

* `benchmark_tasks/calibration_logs/empirical_velocity_calibration_log.json`
* `results/tables/velocity_task_difficulty_rebalanced.csv`
* `results/figures/velocity_task_difficulty_rebalance.png`

The v2 calibration is based on local sample solver profiles. It does not claim frontier-model calibration.

Relevant tests:

* `tests/test_velocity_calibration.py`

## Pipeline Evidence

### v1 pipeline

The v1 benchmark pipeline is orchestrated by:

* `src/cellfatebench/pipeline.py`
* `scripts/08_run_full_pipeline.py`

Command:

`make pipeline`

Expected output:

`CellFateBench full pipeline completed. All expected outputs are present.`

### v2 pipeline

The v2 public RNA velocity pipeline is orchestrated by:

* `src/cellfatebench/v2_pipeline.py`
* `scripts/12_run_v2_pipeline.py`

Command:

`make pipeline-v2`

Expected output:

`CellFateBench v2 public RNA velocity pipeline completed. All expected v2 outputs are present.`

## Visual Evidence

Generated figures:

* `results/figures/synthetic_spatial_layout.png`
* `results/figures/pseudotime_by_branch.png`
* `results/figures/task_family_counts.png`
* `results/figures/sample_solver_scores.png`
* `results/figures/velocity_solver_score_by_profile.png`
* `results/figures/velocity_task_pass_rate.png`
* `results/figures/velocity_task_difficulty_rebalance.png`

Generated summary tables:

* `results/tables/benchmark_task_summary.csv`
* `results/tables/topology_summary.json`
* `results/tables/velocity_dataset_summary.csv`
* `results/tables/velocity_layer_summary.csv`
* `results/tables/velocity_solver_performance_summary.csv`
* `results/tables/velocity_task_performance_summary.csv`
* `results/tables/velocity_task_difficulty_rebalanced.csv`

## Docker Evidence

Docker support is provided by:

* `Dockerfile`
* `.dockerignore`

Docker validation commands:

* `docker build -t cellfatebench:latest .`
* `docker run --rm cellfatebench:latest make test`
* `docker run --rm cellfatebench:latest make pipeline`
* `docker run --rm cellfatebench:latest make pipeline-v2`

GitHub Actions validates Docker execution.

## CI Evidence

CI workflow:

* `.github/workflows/ci.yml`

The CI workflow validates:

* `make test`;
* `make pipeline`;
* `make pipeline-v2`;
* expected v1 output files;
* expected v2 output files;
* Docker build;
* Docker test execution;
* Docker v1 pipeline execution;
* Docker v2 pipeline execution.

Recent CI runs have passed on `main`.

## Reviewer Reproduction Checklist

A reviewer can reproduce the project with:

* `conda env create -f environment.yml`
* `conda activate cellfatebench`
* `make test`
* `make pipeline`
* `make pipeline-v2`

For container-level validation:

* `docker build -t cellfatebench:latest .`
* `docker run --rm cellfatebench:latest make test`
* `docker run --rm cellfatebench:latest make pipeline`
* `docker run --rm cellfatebench:latest make pipeline-v2`

## Evidence Boundaries

The project is intentionally clear about what is and is not claimed.

Supported claims:

* v1 synthetic hidden truth is controlled and deterministic.
* v2 public RNA velocity dataset summaries are reproducibly generated.
* Public tasks are separated from hidden answers.
* Oracle outputs are provided for inspection.
* v1 and v2 pipelines run locally and in CI.
* Docker validation is supported.
* v2 calibration is based on local sample solver profiles.

Unsupported claims:

* clinical or diagnostic validity;
* full biological discovery from the synthetic dataset;
* full scVelo velocity-graph computation inside the current v2 benchmark pipeline;
* empirical frontier-model calibration;
* replacement of expert biological review.
