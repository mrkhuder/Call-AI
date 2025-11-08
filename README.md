# CareFlow AI

CareFlow AI brings frictionless scheduling to healthcare systems by combining predictive analytics, multi-channel patient engagement, and automated waitlist orchestration. The platform reduces no-shows, unlocks clinical capacity, and makes it easier for patients to access timely care.

## Monorepo Structure

- `backend/` – FastAPI service exposing scheduling, reminders, waitlist, and analytics APIs.
- `frontend/` – Vite + React patient/provider experience for mobile/web surfaces.
- `ml/` – Notebooks and pipelines for the no-show risk model and demand forecasting.
- `infra/` – Placeholder for cloud infrastructure as code and deployment manifests.
- `docs/` – Design notes, runbooks, and integration guides.

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- Poetry or pip (for backend dependencies)

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger UI will be available at `http://localhost:8000/docs`.

Database migrations (Alembic) run automatically on API startup. To manage them manually:

```bash
alembic -c alembic.ini upgrade head      # apply migrations
alembic -c alembic.ini revision --autogenerate -m "describe change"
```

#### Tests

```bash
cd backend
pytest
```

The bundled `pytest.ini` enables quiet reporting and configures import paths, making it CI-ready out of the box.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` to view the CareFlow AI experience.

### Machine Learning Pipelines

```bash
cd ml
python -m pipelines.no_show --config config.yml
```

The command trains a baseline no-show classifier (using synthetic data if a source dataset is absent) and drops artifacts in `ml/models/no_show_v1/`.

### Docker (Optional)

Spin up the full stack with hot-reload friendly containers:

```bash
docker compose up --build
```

Run the ML training container on demand:

```bash
docker compose run --rm --profile ml ml-pipeline
```

## Key Capabilities (Initial Slice)

- **Self-Scheduling API** – Validates requests, produces personalized slot suggestions, and scores no-show risk.
- **Reminders & Outreach** – Schedules multi-channel reminders, persists delivery metadata, and routes dispatch through a provider abstraction (mock today).
- **Waitlist Automation** – Registers patient preferences and simulates rapid-fill notifications when slots open.
- **Analytics** – Provides demand forecasting stubs and interpretable no-show risk summaries.
- ML pipeline artifacts (`ml/models/no_show_v1/pipeline.pkl`) are auto-loaded by the API when available, with heuristics as a safety fallback.

## Next Steps

1. Connect to the EHR sandbox via the integration adapter layer (`backend/app/services/scheduling_service.py`).
2. Replace the mock no-show risk scorer with the trained pipeline served via the ML microservice.
3. Expand ReminderService with Twilio/SendGrid integrations and compliance auditing.
4. Harden waitlist prioritisation with business rules, fairness checks, and audit logging.
5. Build IVR flow definitions and speech model integration for the AI-powered phone system.

## Security & Compliance

- Do not commit PHI/PII. Keep anonymised IDs in shared environments.
- Configure `.env` with secrets (database URL, messaging credentials) and never check it into source control.
- Ensure audit trails for automated outreach, overbooking decisions, and waitlist fills.
