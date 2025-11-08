from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterable, List, Protocol

from ..core.config import settings


class BaseEHRClient(Protocol):
    async def push_appointment(self, payload: "EHRAppointmentPayload") -> None:
        ...

    async def get_available_slots(self, query: "EHRSlotQuery") -> Iterable["EHRSlot"]:
        ...


@dataclass
class EHRAppointmentPayload:
    appointment_id: str
    patient_id: str
    provider_id: str
    start: datetime
    end: datetime
    reason: str
    location_id: str | None


@dataclass
class EHRSlotQuery:
    provider_id: str | None
    visit_type: str | None
    start_after: datetime
    end_before: datetime


@dataclass
class EHRSlot:
    provider_id: str
    slot_start: datetime
    slot_end: datetime
    location_id: str


class MockEHRClient:
    """
    Mock EHR client that emulates a scheduling system.
    Generates slots around business hours and logs outgoing appointments.
    """

    async def push_appointment(self, payload: EHRAppointmentPayload) -> None:  # pragma: no cover - side-effects only
        # In real implementation, this would POST to the EHR scheduling API.
        print(
            f"[MockEHR] Registered appointment {payload.appointment_id} for patient {payload.patient_id} "
            f"with provider {payload.provider_id} at {payload.start.isoformat()}."
        )

    async def get_available_slots(self, query: EHRSlotQuery) -> List[EHRSlot]:
        slots: list[EHRSlot] = []
        current = query.start_after
        while current < query.end_before:
            slot_start = current.replace(hour=9, minute=0, second=0, microsecond=0)
            for offset in range(3):
                start = slot_start + timedelta(days=offset)
                end = start + timedelta(minutes=30)
                slots.append(
                    EHRSlot(
                        provider_id=query.provider_id or "provider-123",
                        slot_start=start,
                        slot_end=end,
                        location_id="loc-1",
                    )
                )
            current += timedelta(days=7)
        return slots


def get_ehr_client() -> BaseEHRClient:
    """
    Factory for retrieving the active EHR client based on feature flags/environment.
    """
    if settings.feature_flags.get("use_mock_ehr", True):
        return MockEHRClient()

    raise NotImplementedError("Real EHR client not implemented yet.")
