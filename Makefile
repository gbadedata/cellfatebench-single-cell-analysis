PYTHONPATH := src

.PHONY: test dataset trajectory spatial topology-summary topology-tasks calibration score pipeline velocity-data velocity-tasks pipeline-v2

test:
	PYTHONPATH=$(PYTHONPATH) pytest -q

dataset:
	PYTHONPATH=$(PYTHONPATH) python scripts/01_generate_synthetic_dataset.py

trajectory:
	PYTHONPATH=$(PYTHONPATH) python scripts/02_generate_trajectory_tasks.py

spatial:
	PYTHONPATH=$(PYTHONPATH) python scripts/03_generate_spatial_tasks.py

topology-summary:
	PYTHONPATH=$(PYTHONPATH) python scripts/04_generate_topology_summary.py

topology-tasks:
	PYTHONPATH=$(PYTHONPATH) python scripts/05_generate_topology_tasks.py

calibration:
	PYTHONPATH=$(PYTHONPATH) python scripts/07_generate_calibration_log.py

score:
	PYTHONPATH=$(PYTHONPATH) python scripts/06_score_sample_solver_answers.py

pipeline:
	PYTHONPATH=$(PYTHONPATH) python scripts/08_run_full_pipeline.py

velocity-data:
	PYTHONPATH=$(PYTHONPATH) python scripts/10_prepare_public_velocity_dataset.py

velocity-tasks:
	PYTHONPATH=$(PYTHONPATH) python scripts/11_generate_velocity_tasks.py

pipeline-v2:
	PYTHONPATH=$(PYTHONPATH) python scripts/12_run_v2_pipeline.py

