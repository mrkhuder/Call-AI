from __future__ import annotations

from fastapi import APIRouter, Depends

from ....schemas.scheduling import (
    AppointmentCreateRequest,
    AppointmentResponse,
    AppointmentSuggestion,
    AppointmentSuggestionRequest,
)
from ....services import SchedulingService
from ....services.no_show_model import NoShowRiskModel


def get_scheduling_service() -> SchedulingService:
    return SchedulingService(model=NoShowRiskModel())


router = APIRouter()


@router.post("/", response_model=AppointmentResponse)
async def create_or_update_appointment(
    payload: AppointmentCreateRequest, service: SchedulingService = Depends(get_scheduling_service)
) -> AppointmentResponse:
    return await service.schedule_appointment(payload)


@router.post("/suggestions", response_model=list[AppointmentSuggestion])
async def appointment_suggestions(
    payload: AppointmentSuggestionRequest, service: SchedulingService = Depends(get_scheduling_service)
) -> list[AppointmentSuggestion]:
    return await service.suggest_appointments(payload)
