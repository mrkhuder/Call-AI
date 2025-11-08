from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel import Session

from ....schemas.reminders import ReminderCreate, ReminderResponse
from ....db.session import get_session
from ....integrations.messaging import get_messaging_provider
from ....services import ReminderService


def get_reminder_service(session: Session = Depends(get_session)) -> ReminderService:
    messaging_provider = get_messaging_provider()
    return ReminderService(session=session, messaging_provider=messaging_provider)


router = APIRouter()


@router.post("/", response_model=ReminderResponse)
async def schedule_reminder(
    payload: ReminderCreate, service: ReminderService = Depends(get_reminder_service)
) -> ReminderResponse:
    return await service.schedule_reminder(payload)
