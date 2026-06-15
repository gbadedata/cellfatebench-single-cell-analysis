# Project Design

## Project Title

CellFateBench: A Single-Cell Benchmark for Trajectory, Spatial, and Topological Analysis

## Purpose

CellFateBench is designed as a benchmark suite for evaluating reasoning over single-cell genomics workflows.

The project focuses on three reasoning areas:

1. trajectory and pseudotime reasoning;
2. spatial gene-pattern reasoning;
3. topological persistence reasoning.

## Why Controlled Synthetic Data?

The project uses controlled synthetic single-cell scenarios because benchmark tasks need known hidden truth.

For example, if a task asks a solver to infer the starting cell state, terminal state, hidden branch, spatial domain, or persistent topological feature, the benchmark must know the correct answer.

Controlled synthetic data allows the project to define:

- true cell states;
- true pseudotime order;
- true branch membership;
- true spatial domains;
- true spatially variable genes;
- true topological structures.

This makes the benchmark evaluable rather than merely descriptive.

## Benchmark Components

The project will include:

- public task prompts;
- hidden answer keys;
- oracle outputs;
- validator functions;
- scoring functions;
- calibration logs;
- difficulty labels;
- evidence files;
- visual outputs;
- reproducibility tooling.

## Scientific Scope

This project is not a clinical or diagnostic workflow.

It is a scientific software and benchmark-design project for demonstrating single-cell reasoning, reproducibility, and evaluation design.
