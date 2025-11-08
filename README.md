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

## Key Capabilities (Initial Slice)

- **Self-Scheduling API** – Validates requests, produces personalized slot suggestions, and scores no-show risk.
- **Reminders & Outreach** – Schedules multi-channel reminders and adapts cadence based on risk profile.
- **Waitlist Automation** – Registers patient preferences and simulates rapid-fill notifications when slots open.
- **Analytics** – Provides demand forecasting stubs and interpretable no-show risk summaries.

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
