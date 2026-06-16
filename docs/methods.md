# Methods

## Project Overview

CellFateBench is a reproducible benchmark-design project for evaluating scientific reasoning over single-cell genomics workflows.

The project converts single-cell analysis scenarios into structured benchmark assets:

* public benchmark tasks;
* hidden answer keys;
* oracle outputs;
* deterministic validators;
* scoring reports;
* calibration logs;
* difficulty rebalancing outputs;
* reproducible pipelines;
* Docker and CI validation;
* reviewer-ready documentation.

CellFateBench currently contains two benchmark layers:

| Layer                            | Description                                                                                                                                                 | Status   |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| v1 controlled benchmark          | Synthetic single-cell benchmark with known hidden truth across trajectory, spatial, and topology reasoning tasks                                            | Complete |
| v2 public RNA velocity extension | Public scVelo pancreas RNA velocity benchmark extension with velocity reasoning tasks, solver evaluation, empirical calibration, and difficulty rebalancing | Complete |

The project is designed to demonstrate scientific software engineering, benchmark construction, reproducible analysis, and evaluation methodology in computational biology.

## Methodological Rationale

Single-cell workflows produce outputs such as embeddings, clusters, marker summaries, pseudotime estimates, spatial patterns, topology summaries, and RNA velocity layers.

However, producing outputs is not the same as interpreting them correctly.

CellFateBench focuses on the reasoning layer. It evaluates whether a solver can:

* combine evidence from multiple single-cell summaries;
* identify the most supported biological interpretation;
* reject unsupported or overconfident claims;
* distinguish similar-looking but scientifically different signals;
* report uncertainty where the evidence is incomplete;
* avoid hidden answer leakage into public task prompts.

This makes CellFateBench a benchmark-engineering project rather than a standard exploratory analysis notebook.

## Data Strategy

CellFateBench uses two complementary data strategies.

### v1 controlled synthetic data

The v1 layer uses controlled synthetic single-cell data.

This was selected because deterministic benchmark evaluation requires known hidden truth. In many real biological datasets, the true trajectory, branch structure, spatial domain assignment, or topology may be uncertain, partially validated, or context-dependent.

Synthetic data allows the benchmark to define known answers for:

* root or progenitor state;
* transition state;
* terminal branch states;
* branch labels;
* pseudotime values;
* spatial coordinates;
* spatial domains;
* spatially variable gene programmes;
* topology design.

This supports deterministic validation and hidden-answer scoring.

### v2 public RNA velocity data

The v2 layer adds a public RNA velocity dataset based on the scVelo pancreas dataset.

The public dataset layer validates:

* 3,696 cells;
* 27,998 genes;
* spliced layer;
* unspliced layer;
* cluster annotation column;
* 8 annotation groups.

The project does not commit large raw public data files. Instead, it loads the public dataset through code and commits lightweight derived outputs such as dataset summaries, layer summaries, task files, solver summaries, calibration logs, and figures.

This keeps the repository lightweight while preserving reproducibility.

## v1 Synthetic Dataset Design

The v1 synthetic dataset contains:

| Feature                | Value |
| ---------------------- | ----: |
| Synthetic cells        |   900 |
| Genes                  |    60 |
| Designed branch labels |     4 |
| Spatial domains        |     5 |
| Terminal states        |     2 |

The generated dataset includes:

* cell metadata;
* expression matrix;
* gene metadata;
* hidden truth JSON;
* pseudotime summaries;
* spatial coordinate structure;
* topology-oriented design.

Generated files include:

* `data/synthetic/synthetic_cell_metadata.csv`
* `data/synthetic/synthetic_expression_matrix.csv`
* `data/synthetic/synthetic_gene_metadata.csv`
* `data/synthetic/synthetic_hidden_truth.json`

## v1 Gene Programme Design

The v1 dataset includes designed gene programmes for:

* root or progenitor state;
* transition state;
* branch A terminal state;
* branch B terminal state;
* cycling-like signal;
* left spatial domain;
* right spatial domain;
* ring-like spatial domain.

These programmes support reasoning tasks where solvers must infer biological structure from partial evidence.

## v1 Benchmark Task Families

### 1. Trajectory and pseudotime reasoning

Trajectory tasks evaluate whether a solver can reason about:

* likely root state;
* terminal states;
* early-to-late pseudotime ordering;
* transition-state placement;
* masked terminal-state recovery.

These tasks require combining marker evidence with pseudotime evidence.

Files:

* `benchmark_tasks/public/trajectory_pseudotime_tasks.json`
* `benchmark_tasks/hidden/trajectory_pseudotime_answers.json`
* `benchmark_tasks/oracle_outputs/trajectory_pseudotime_oracle_outputs.json`

### 2. Spatial pattern reasoning

Spatial tasks evaluate whether a solver can reason about:

* spatially variable gene groups;
* domain-specific marker enrichment;
* masked spatial-domain recovery;
* false-positive spatial claims.

These tasks test whether a solver can separate true spatial-domain evidence from unrelated expression programmes.

Files:

* `benchmark_tasks/public/spatial_pattern_tasks.json`
* `benchmark_tasks/hidden/spatial_pattern_answers.json`
* `benchmark_tasks/oracle_outputs/spatial_pattern_oracle_outputs.json`

### 3. Topological persistence reasoning

Topological tasks evaluate whether a solver can reason about:

* bifurcating trajectory structure;
* major branch count;
* spatial ring-signal interpretation;
* false-positive loop claims;
* the distinction between spatial topology and cell-fate topology.

The project uses GUDHI to compute lightweight persistent-homology summaries from coordinate-derived point clouds.

Files:

* `benchmark_tasks/public/topological_persistence_tasks.json`
* `benchmark_tasks/hidden/topological_persistence_answers.json`
* `benchmark_tasks/oracle_outputs/topological_persistence_oracle_outputs.json`

## v2 Public RNA Velocity Extension

The v2 layer extends the benchmark with RNA velocity reasoning.

The purpose of v2 is not simply to run scVelo. The purpose is to convert RNA velocity dataset context into benchmark tasks that test scientific reasoning, evidence discipline, and uncertainty handling.

v2 adds:

* public scVelo pancreas dataset preparation;
* spliced and unspliced layer validation;
* annotation-column inference;
* dataset summary outputs;
* RNA velocity reasoning task generation;
* hidden answer keys;
* oracle outputs;
* solver profiles;
* expanded scoring;
* solver performance reports;
* empirical calibration;
* difficulty rebalancing;
* a dedicated v2 pipeline.

## v2 Dataset Preparation

The public velocity dataset preparation is implemented in:

* `src/cellfatebench/public_velocity.py`
* `scripts/10_prepare_public_velocity_dataset.py`

Generated outputs:

* `results/tables/velocity_dataset_summary.csv`
* `results/tables/velocity_layer_summary.csv`

The dataset validation checks:

* required velocity layers are present;
* spliced and unspliced layers match the AnnData shape;
* annotation columns can be identified;
* lightweight summary files are written for review.

## v2 Velocity Task Design

Velocity task generation is implemented in:

* `src/cellfatebench/velocity_tasks.py`
* `scripts/11_generate_velocity_tasks.py`

Generated benchmark files:

* `benchmark_tasks/public/velocity_reasoning_tasks.json`
* `benchmark_tasks/hidden/velocity_reasoning_answers.json`
* `benchmark_tasks/oracle_outputs/velocity_reasoning_oracle_outputs.json`

The current v2 task set includes six RNA velocity reasoning tasks.

The tasks evaluate whether a solver can reason about:

* upstream or progenitor-like states;
* terminal endocrine fate support;
* contradiction detection;
* latent-time-style ordering;
* low-confidence failure modes;
* marker and velocity evidence alignment.

The tasks are intentionally careful about evidence boundaries. They do not claim that layer availability alone proves full velocity direction, latent time, or transition probability.

## Public Task and Hidden Answer Separation

Each task family separates public prompts from hidden answer keys.

Public tasks contain the visible problem statement and observable evidence.

Hidden answers contain:

* expected answer;
* expected claim;
* required evidence terms;
* acceptable reasoning fields;
* scoring-relevant metadata.

This separation supports benchmark-style evaluation and reduces answer leakage.

The repository also includes tests that check public task files do not expose hidden answer-key fields.

## Oracle Outputs

Oracle outputs provide reference-style answers for each task family.

They include:

* expected conclusion;
* confidence level;
* rationale;
* supporting evidence;
* uncertainty or limitation notes where relevant.

Oracle outputs are not used as public prompts. They exist to support inspection, future solver evaluation, and reviewer understanding.

## Scoring Methodology

CellFateBench uses transparent scoring.

The v1 scoring system supports:

* expected answer matching;
* Boolean claim correctness;
* required evidence-term coverage;
* confidence field presence;
* partial credit.

The v2 velocity scoring system adds:

* correctness scoring;
* evidence-support scoring;
* uncertainty-discipline scoring;
* no-overclaim discipline;
* penalty for unsupported precision or certainty claims.

Velocity solver evaluation is implemented in:

* `src/cellfatebench/velocity_solver_evaluation.py`
* `scripts/13_evaluate_velocity_solvers.py`

Generated outputs:

* `results/tables/velocity_solver_performance_summary.csv`
* `results/tables/velocity_task_performance_summary.csv`
* `results/figures/velocity_solver_score_by_profile.png`
* `results/figures/velocity_task_pass_rate.png`

## Calibration Methodology

CellFateBench includes two calibration layers.

### v1 design-stage calibration

The v1 calibration log documents:

* declared task difficulty;
* reasoning requirements;
* likely solver failure modes;
* calibration recommendations;
* empirical calibration status.

Implemented in:

* `src/cellfatebench/calibration.py`

Generated output:

* `benchmark_tasks/calibration_logs/design_stage_calibration_log.json`

### v2 empirical sample-solver calibration

The v2 calibration layer reviews RNA velocity task difficulty using local sample solver profiles.

Implemented in:

* `src/cellfatebench/velocity_calibration.py`
* `scripts/14_generate_velocity_calibration.py`

Generated outputs:

* `benchmark_tasks/calibration_logs/empirical_velocity_calibration_log.json`
* `results/tables/velocity_task_difficulty_rebalanced.csv`
* `results/figures/velocity_task_difficulty_rebalance.png`

Important scope note:

The project does not claim frontier-model calibration. v2 empirical calibration is based on local sample solver profiles and is used to demonstrate benchmark-engineering methodology.

## Reproducibility

The v1 benchmark pipeline can be regenerated with:

`make pipeline`

The v2 public RNA velocity pipeline can be regenerated with:

`make pipeline-v2`

The test suite can be run with:

`make test`

Docker reproducibility is supported with:

* `docker build -t cellfatebench:latest .`
* `docker run --rm cellfatebench:latest make test`
* `docker run --rm cellfatebench:latest make pipeline`
* `docker run --rm cellfatebench:latest make pipeline-v2`

GitHub Actions CI validates:

* tests;
* v1 pipeline;
* v2 pipeline;
* expected v1 outputs;
* expected v2 outputs;
* Docker build;
* Docker tests;
* Docker v1 pipeline;
* Docker v2 pipeline.

## Testing Strategy

The test suite validates:

* synthetic dataset generation;
* public task generation;
* hidden-answer separation;
* oracle output creation;
* topology summaries;
* scoring logic;
* calibration logic;
* visual output generation;
* v1 pipeline orchestration;
* public velocity dataset validation;
* velocity task generation;
* velocity solver evaluation;
* velocity calibration;
* v2 pipeline orchestration.

Current local validation status:

`57 passed`

The public scVelo pancreas dataset can emit AnnData old-format warnings because the upstream dataset file uses older H5AD metadata conventions. These warnings do not indicate failure of the CellFateBench logic.

## Scope and Limitations

CellFateBench is not a clinical diagnostic workflow.

It is a scientific software and benchmark-design project for demonstrating:

* single-cell reasoning;
* benchmark task design;
* hidden-answer evaluation;
* reproducibility;
* calibration methodology;
* evidence-based documentation.

The project does not replace expert biological interpretation or experimental validation.
