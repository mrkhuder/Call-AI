from __future__ import annotations

from fastapi import APIRouter, Depends

from ....schemas.reminders import ReminderCreate, ReminderResponse
from ....services import ReminderService


def get_reminder_service() -> ReminderService:
    return ReminderService()


router = APIRouter()


@router.post("/", response_model=ReminderResponse)
async def schedule_reminder(
    payload: ReminderCreate, service: ReminderService = Depends(get_reminder_service)
) -> ReminderResponse:
    return await service.schedule_reminder(payload)
