# Methods

## Project Overview

CellFateBench is a benchmark-design project for evaluating reasoning over single-cell genomics workflows.

The benchmark focuses on three analysis settings:

1. trajectory and pseudotime reasoning;
2. spatial gene-pattern reasoning;
3. topological persistence reasoning.

The project demonstrates how single-cell analysis outputs can be transformed into structured benchmark tasks with public prompts, hidden answer keys, oracle outputs, deterministic validators, partial-credit scoring, calibration logs, reproducible execution, Docker support, and CI validation.

## Dataset Design

CellFateBench uses a controlled synthetic single-cell dataset.

This design was selected because benchmark tasks require known hidden truth. In many real biological datasets, the true trajectory, branch membership, spatial domains, and topological structure may be uncertain or only partially validated. A controlled synthetic dataset allows the benchmark to define known answers for evaluation.

The generated dataset contains:

* 900 synthetic cells;
* 60 genes;
* known root/progenitor state;
* known transition state;
* two known terminal branches;
* known pseudotime values;
* known spatial coordinates;
* known spatial domains;
* known spatially variable gene groups;
* known topological design.

## Gene Programme Design

The dataset includes designed gene programmes for:

* root/progenitor state;
* transition state;
* branch A terminal state;
* branch B terminal state;
* cycling-like signal;
* left spatial domain;
* right spatial domain;
* ring-like spatial domain.

These gene programmes support benchmark tasks where solvers must infer cell-state identity, branch structure, spatial patterning, or false-positive interpretations from partial evidence.

## Trajectory and Pseudotime Tasks

Trajectory tasks evaluate whether a solver can reason about:

* the likely root state;
* terminal states;
* early-to-late pseudotime ordering;
* transition-state placement;
* masked terminal-state recovery.

These tasks require combining marker evidence with pseudotime summaries. They are not simple label-recall exercises.

## Spatial Pattern Tasks

Spatial tasks evaluate whether a solver can reason about:

* spatially variable gene groups;
* domain-specific marker enrichment;
* masked spatial-domain recovery;
* false-positive spatial claims.

The benchmark separates true spatial-domain signals from other expression programmes so that unsupported interpretations can be tested.

## Topological Persistence Tasks

Topological tasks evaluate whether a solver can reason about:

* bifurcating trajectory structure;
* major branch count;
* spatial ring-signal interpretation;
* false-positive loop claims;
* the distinction between spatial topology and cell-fate topology.

The project uses GUDHI to compute lightweight persistent-homology summaries from coordinate-derived point clouds.

## Public Tasks and Hidden Answers

Each task family contains public task files and hidden answer files.

Public task files contain the visible problem statements and observable data. Hidden answer files contain expected labels, expected claims, acceptable evidence terms, and scoring-relevant fields.

This separation helps prevent answer leakage and makes the benchmark structure more credible.

## Oracle Outputs

Each task family includes oracle outputs.

Oracle outputs provide reference-style answers, including:

* expected conclusion;
* confidence level;
* rationale;
* supporting evidence.

These outputs make the benchmark easier to inspect and support future solver evaluation.

## Scoring

The scoring system supports partial credit.

The current scoring checks:

* expected answer or claim match;
* Boolean claim correctness where relevant;
* required evidence-term coverage;
* confidence field presence.

The sample solver answer set validates the scoring pipeline and generates a reviewable score report.

## Calibration

The project includes a design-stage calibration log.

This calibration layer documents:

* declared task difficulty;
* reasoning requirements;
* likely solver failure modes;
* calibration recommendations;
* empirical calibration status.

The project does not claim empirical frontier-model calibration. The current calibration log is a design-stage review asset. Future versions can add empirical model or human-solver calibration results.

## Reproducibility

The benchmark can be regenerated end to end with:

```bash
make pipeline
```

The test suite can be run with:

```bash
make test
```

Docker reproducibility is supported with:

```bash
docker build -t cellfatebench:latest .
docker run --rm cellfatebench:latest make test
docker run --rm cellfatebench:latest make pipeline
```

GitHub Actions CI runs tests, the full pipeline, and Docker validation.

## Scope and Limitations

CellFateBench is not a clinical or diagnostic workflow.

It is a scientific software and benchmark-design project for demonstrating single-cell reasoning, reproducibility, and evaluation design.

The first version uses controlled synthetic data because the benchmark needs known hidden truth. Future versions can add public real-world single-cell datasets after the benchmark framework is established.
