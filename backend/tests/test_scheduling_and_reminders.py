from __future__ import annotations

from datetime import datetime, timedelta

import pytest
from sqlmodel import Session, select

from app.models import Appointment, Reminder


def test_schedule_appointment_persists_record(client, engine):
    payload = {
        "patient_id": "patient-001",
        "provider_id": "provider-123",
        "reason_for_visit": "Follow-up consultation",
        "appointment_start": datetime.utcnow().replace(microsecond=0).isoformat(),
        "appointment_end": (datetime.utcnow() + timedelta(minutes=30)).replace(microsecond=0).isoformat(),
        "channel": "mobile",
        "insurance_plan": "premium",
        "location_id": "loc-100",
    }

    response = client.post("/api/v1/scheduling/", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["appointment_id"]
    assert data["status"] in {"confirmed", "pending"}
    assert 0 <= data["no_show_risk"] <= 1

    with Session(engine) as session:
        appointment = session.exec(select(Appointment)).first()
        assert appointment is not None
        assert appointment.id == data["appointment_id"]
        assert appointment.patient_id == payload["patient_id"]
        assert appointment.no_show_risk == pytest.approx(data["no_show_risk"])


def test_reminder_persists_and_dispatches(client, engine, sent_reminders):
    schedule_payload = {
        "patient_id": "patient-002",
        "provider_id": "provider-789",
        "reason_for_visit": "Dermatology check",
        "appointment_start": datetime.utcnow().replace(microsecond=0).isoformat(),
        "appointment_end": (datetime.utcnow() + timedelta(minutes=20)).replace(microsecond=0).isoformat(),
        "channel": "web",
        "insurance_plan": "standard",
        "location_id": "loc-201",
    }
    schedule_response = client.post("/api/v1/scheduling/", json=schedule_payload)
    appointment_id = schedule_response.json()["appointment_id"]

    reminder_payload = {
        "appointment_id": appointment_id,
        "patient_id": schedule_payload["patient_id"],
        "channel": "sms",
        "send_at": (datetime.utcnow() + timedelta(hours=1)).replace(microsecond=0).isoformat(),
        "template_id": "reminder-standard",
        "high_risk": True,
        "additional_context": "Bring previous lab results.",
    }

    response = client.post("/api/v1/reminders/", json=reminder_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["reminder_id"]
    assert data["status"] in {"scheduled", "sent"}

    assert len(sent_reminders) == 1
    assert sent_reminders[0].reminder_id == data["reminder_id"]
    assert sent_reminders[0].channel == reminder_payload["channel"]

    with Session(engine) as session:
        reminder = session.exec(select(Reminder)).first()
        assert reminder is not None
        assert reminder.id == data["reminder_id"]
        assert reminder.patient_id == reminder_payload["patient_id"]
        assert reminder.status == data["status"]
