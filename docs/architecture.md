# CareFlow AI – Technical Architecture (Initial Cut)

## Overview

CareFlow AI orchestrates scheduling intelligence across three workstreams:

1. **Operational APIs** (FastAPI) – Surface appointment booking, reminders, waitlist automations, and analytics required by patient- and staff-facing channels.
2. **Patient Experience** (Vite + React) – Deliver a unified mobile/web experience with AI-informed slot suggestions and proactive outreach.
3. **Intelligence Layer** (Python ML pipelines) – Train, evaluate, and monitor predictive models for no-show risk and demand forecasting.

## Backend Service

- **Framework**: FastAPI + Uvicorn.
- **Modules**:
  - `api.v1.scheduling` – Books appointments and retrieves personalized suggestions.
  - `api.v1.reminders` – Schedules multi-channel reminders.
  - `api.v1.waitlist` – Registers preferences and triggers 15-minute claim notifications.
  - `api.v1.analytics` – Returns no-show risk explanations and forecast data.
- **Services Layer** sits in `app/services`:
  - `SchedulingService` coordinates EHR integration (currently mocked) and calls the no-show model.
  - `ReminderService` prepares reminder payloads and delegates delivery to a messaging provider abstraction.
  - `WaitlistService` manages eligibility and messaging for openings.
  - `AnalyticsService` aggregates model outputs and forecasting heuristics.
- **Integrations** (`app/integrations`):
  - `MockEHRClient` simulates a FHIR-compatible scheduling system. It can be swapped for a real adapter when ready.
  - `MockMessagingProvider` emulates SMS/e-mail delivery; replace with Twilio/SendGrid providers behind the shared interface.
- **Configuration**: `app/core/config.py` uses Pydantic Settings to load environment variables (`.env`).
- **Logging**: Structured logging via `logging.config.dictConfig`.
- **Testing**: `backend/tests/test_health.py` ensures base health endpoint coverage.

### Integration Points (Future)

- EHR connectivity via FHIR Scheduling and Appointment resources.
- Messaging providers (Twilio, SendGrid) for reminders.
- Speech stack (ASR + NLU) for AI-powered IVR.
- MLOps platform for model serving (e.g., BentoML, Sagemaker, Vertex AI).

## Frontend Application

- **Stack**: Vite, React 18, TypeScript, React Query.
- **Atomic Components**:
  - `BookingForm` – 3-click booking workflow mirroring mobile experience.
  - `SuggestionPanel` – Displays preference-tailored slots.
  - `NoShowRiskCard` – Surfaces risk insights/tiers for upcoming appointments.
  - `WaitlistCard` – Collects waitlist preferences and simulates outreach.
- **State/Data**: Axios client wraps API calls, React Query manages request lifecycle and caching.
- **Styling**: Custom CSS in `App.css` designed for clean, accessible UI without Tailwind dependency.
- **Proxy**: Vite dev server proxies `/api` calls to FastAPI (`vite.config.ts`).

## Machine Learning Layer

- `pipelines/no_show.py` – Reference training script that:
  - Loads configuration from `ml/config.yml`.
  - Reads dataset from `ml/data/appointments.csv` or generates synthetic data for development.
  - Builds feature preprocessing (OneHot + scaling) and trains Gradient Boosting model.
  - Saves pipeline artifact and metrics to `ml/models/no_show_v1/`.
- The FastAPI service lazily loads the pipeline artifact (when present) to score appointments in real time, falling back to heuristics if unavailable.
- Future enhancements:
  - Replace synthetic data generator with production EHR extracts.
  - Introduce feature/store integration and drift monitoring.
  - Automate retraining schedule and CI/CD gating for model rollout.

## Security & Compliance

- HIPAA-aligned design with audit logging, encryption, and least-privilege credential management.
- `.env` (unsynced) to hold secrets: database URL, broker, API tokens.
- Planned Data Governance: PHI tokenization, access audits, role-based dashboards.

## Deployment Considerations

- Containerisation via Docker (to be added) with multi-stage builds.
- Infrastructure targets: Kubernetes or serverless (AWS Fargate) for API, managed Postgres, Redis, and message queue.
- Observability: Structured logs, Prometheus metrics, OpenTelemetry traces for cross-service insights.
- CI/CD: GitHub Actions / Azure DevOps pipelines to lint/test (backend + frontend + ML), build images, and push to artifact registry.
