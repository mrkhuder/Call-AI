from fastapi import APIRouter

from .endpoints import scheduling, reminders, waitlist, analytics

api_router = APIRouter()

api_router.include_router(scheduling.router, prefix="/scheduling", tags=["scheduling"])
api_router.include_router(reminders.router, prefix="/reminders", tags=["reminders"])
api_router.include_router(waitlist.router, prefix="/waitlist", tags=["waitlist"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
