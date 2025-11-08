from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel import Session

from ....schemas.scheduling import (
    AppointmentCreateRequest,
    AppointmentResponse,
    AppointmentSuggestion,
    AppointmentSuggestionRequest,
)
from ....db.session import get_session
from ....integrations.ehr import get_ehr_client
from ....services import SchedulingService
from ....services.no_show_model import NoShowRiskModel


def get_scheduling_service(
    session: Session = Depends(get_session),
) -> SchedulingService:
    ehr_client = get_ehr_client()
    return SchedulingService(session=session, model=NoShowRiskModel(), ehr_client=ehr_client)


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
