# CareFlow AI - ML Pipelines

This module contains the data science workflows that power CareFlow AI.

## No-Show Risk Model (V1)

- **Objective**: Predict the probability that a patient misses a scheduled appointment.
- **Input Features** (initial set):
  - Demographics: age, gender, zip-code derived distance.
  - Appointment metadata: lead time, provider specialty, visit type, channel.
  - Historical behaviour: prior no-show rate, cancellation streak, time-of-day adherence.
- **Labels**: binary show/no-show outcome from EHR appointment status.

## Repository Layout

- `pipelines/`: Python entrypoints for training/evaluation.
- `data/`: Staging area for extracted training datasets (never commit PHI/PII).
- `models/`: Serialized model artifacts with metadata.
- `notebooks/`: Exploratory analysis and experimentation.
- `config.yml`: Centralised configuration for data paths and hyperparameters.

## Local Development

1. Export anonymised appointment history to `data/appointments.csv`.
2. Create a Python environment with `pip install -r ../backend/requirements.txt`.
3. Run the baseline training pipeline:

   ```bash
   python -m pipelines.no_show --config config.yml
   ```

4. Review metrics output in `models/no_show_v1/metrics.json`.

## Compliance & Security

- All datasets must be de-identified before leaving the EHR environment.
- PHI should remain in secure, access-controlled storage—work with hashed identifiers.
- Audit training runs and model deployments through MLOps tooling (to be integrated).
