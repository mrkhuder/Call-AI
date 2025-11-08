from __future__ import annotations

from fastapi import APIRouter, Depends

from ....schemas.waitlist import WaitlistEntry, WaitlistNotification
from ....services import WaitlistService


def get_waitlist_service() -> WaitlistService:
    return WaitlistService()


router = APIRouter()


@router.post("/", response_model=dict[str, str])
async def register_waitlist(
    payload: WaitlistEntry, service: WaitlistService = Depends(get_waitlist_service)
) -> dict[str, str]:
    waitlist_id = await service.register_entry(payload)
    return {"waitlist_id": waitlist_id}


@router.post("/notify", response_model=WaitlistNotification)
async def generate_waitlist_notification(
    payload: WaitlistEntry, service: WaitlistService = Depends(get_waitlist_service)
) -> WaitlistNotification:
    return await service.generate_notification(payload)
