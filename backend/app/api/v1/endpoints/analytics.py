from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from ....schemas.analytics import DemandForecastResponse, NoShowRiskScore
from ....services import AnalyticsService


def get_analytics_service() -> AnalyticsService:
    return AnalyticsService()


router = APIRouter()


@router.get("/no-show/{appointment_id}", response_model=NoShowRiskScore)
async def no_show_score(
    appointment_id: str, service: AnalyticsService = Depends(get_analytics_service)
) -> NoShowRiskScore:
    return await service.no_show_score(appointment_id)


@router.get("/demand", response_model=list[DemandForecastResponse])
async def demand_forecast(
    specialty: str = Query(..., description="Clinical specialty to forecast."),
    horizon_days: int = Query(7, ge=1, le=30, description="Number of days to forecast."),
    service: AnalyticsService = Depends(get_analytics_service),
) -> list[DemandForecastResponse]:
    return await service.demand_forecast(specialty=specialty, horizon_days=horizon_days)
