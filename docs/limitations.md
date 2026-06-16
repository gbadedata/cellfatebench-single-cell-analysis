# Limitations

CellFateBench is a research, learning, and portfolio benchmark project. It is designed to demonstrate scientific reasoning evaluation, reproducible workflow engineering, and benchmark construction in single-cell genomics.

It is not a clinical, diagnostic, or regulated biomedical workflow.

## Scope Boundaries

CellFateBench should be interpreted as a benchmark-engineering project.

It is intended to show how single-cell analysis contexts can be converted into:

* public benchmark tasks;
* hidden answer keys;
* oracle outputs;
* deterministic validators;
* scoring reports;
* calibration logs;
* difficulty rebalancing outputs;
* reproducible pipelines;
* Docker and CI validation.

It is not intended to produce new biological discoveries or replace expert analysis.

## v1 Synthetic Data Limitations

The v1 benchmark uses controlled synthetic single-cell data.

This is intentional because deterministic benchmark scoring requires known hidden truth. Synthetic data makes it possible to define expected root states, terminal states, pseudotime patterns, spatial domains, marker programmes, and topology design.

However, synthetic data has important limitations:

* it cannot capture the full biological complexity of real single-cell datasets;
* it simplifies technical noise, batch effects, donor variation, and experimental uncertainty;
* it uses designed gene programmes rather than experimentally observed gene regulation;
* it is better suited to benchmark validation than biological discovery;
* it should not be interpreted as evidence about real disease or developmental systems.

The synthetic layer is therefore best understood as a controlled evaluation environment.

## v2 Public RNA Velocity Limitations

The v2 extension adds a public scVelo pancreas RNA velocity dataset layer.

This improves biological realism, but it also has boundaries:

* public dataset annotations are used as reference context, not absolute biological truth;
* the current v2 layer validates spliced and unspliced RNA velocity layers, but does not yet compute a full scVelo velocity graph inside the benchmark pipeline;
* current velocity tasks focus on reasoning from dataset context and benchmark-provided evidence;
* full velocity graph computation, transition probabilities, and latent-time modelling are future improvements;
* the upstream public AnnData file can emit old-format H5AD warnings during tests.

The AnnData warnings do not indicate failure of CellFateBench logic. They reflect older metadata conventions in the public dataset source.

## Calibration Limitations

CellFateBench includes two calibration layers.

The v1 calibration is design-stage calibration. It documents declared difficulty, reasoning requirements, likely solver failure modes, and calibration recommendations.

The v2 calibration is empirical sample-solver calibration. It uses local sample solver profiles to demonstrate how task difficulty can be reviewed and rebalanced.

Current calibration limitations:

* the project does not claim empirical frontier-model calibration;
* the sample solver profiles are local benchmark fixtures;
* task difficulty estimates should be treated as provisional;
* future calibration should include real solver submissions, human expert review, or frontier-model evaluation;
* calibration results should not be treated as final benchmark validity evidence.

## Scoring Limitations

The scoring system is transparent and useful for benchmark demonstration, but it is not a complete evaluation science framework.

Current scoring limitations:

* text matching can miss semantically correct answers expressed in unexpected wording;
* evidence-term matching is useful but not equivalent to expert biological judgement;
* partial-credit scoring may need task-family-specific refinement;
* overclaim penalties are heuristic;
* solver evaluation is currently based on sample profiles rather than large-scale external submissions.

Future versions can improve scoring with richer schemas, semantic matching, adjudication workflows, expert review, and task-specific rubrics.

## Topology Limitations

The topology layer uses lightweight GUDHI-based summaries to support benchmark reasoning tasks.

Current topology limitations:

* the topology outputs are benchmark-oriented rather than a full topological data analysis study;
* persistence summaries are simplified for task generation and interpretation;
* topology tasks focus on reasoning about supported and unsupported claims;
* spatial ring evidence should not be confused with proof of cyclic cell-fate dynamics;
* deeper persistence diagram analysis remains future work.

## Public Data and Provenance Limitations

The public velocity dataset is loaded through code and summarized into lightweight outputs.

This follows good repository practice, but it also means:

* users need internet access or cached data to regenerate public dataset summaries;
* upstream public dataset availability may change;
* public data annotations may reflect the assumptions of the original dataset;
* raw public data are not stored in this repository;
* derived summaries should be interpreted as benchmark support files, not a complete biological analysis.

## Reproducibility Limitations

The project supports local, Docker, and GitHub Actions validation.

Current reproducibility boundaries:

* dependency versions are managed through `environment.yml`, but scientific Python ecosystems can still change over time;
* public dataset download behaviour depends on upstream hosting and package behaviour;
* local runtime may vary by machine resources;
* Docker improves reproducibility but does not remove all external dependency risk;
* CI validates the repository state at commit time, not future changes to remote public datasets.

## Clinical and Ethical Boundaries

CellFateBench should not be used for:

* clinical diagnosis;
* clinical decision support;
* regulated biomedical reporting;
* patient-specific inference;
* treatment recommendation;
* laboratory decision-making;
* replacing experimental validation;
* replacing expert biological interpretation.

The project is for scientific software demonstration and benchmark design only.

## Current Best Use

CellFateBench is best used as evidence of:

* benchmark design skill;
* single-cell genomics reasoning;
* RNA velocity data handling;
* hidden-answer and oracle-output design;
* deterministic validation;
* transparent scoring;
* calibration methodology;
* reproducible pipeline engineering;
* Docker and CI validation;
* documentation discipline.

It should be reviewed as a portfolio-grade scientific software and benchmark-engineering project, not as a biological discovery paper or clinical workflow.

## Future Improvements

Important future improvements include:

* full scVelo velocity graph computation;
* latent time summaries;
* gene-level velocity confidence summaries;
* real solver submissions;
* frontier-model calibration;
* human expert calibration;
* richer task-family-specific scoring;
* semantic answer matching;
* expanded public datasets;
* spatial-neighbourhood reasoning;
* multi-omic benchmark tasks;
* benchmark metadata versioning;
* release versioning;
* dashboard or web-based review interface after the static benchmark is mature.
