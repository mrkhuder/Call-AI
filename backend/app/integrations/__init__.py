"""Integration factories for external systems."""

from .ehr import BaseEHRClient, EHRAppointmentPayload, EHRSlot, EHRSlotQuery, MockEHRClient, get_ehr_client
from .messaging import MessagingProvider, MockMessagingProvider, ReminderDispatch, get_messaging_provider

__all__ = [
    "BaseEHRClient",
    "EHRAppointmentPayload",
    "EHRSlot",
    "EHRSlotQuery",
    "MockEHRClient",
    "get_ehr_client",
    "MessagingProvider",
    "MockMessagingProvider",
    "ReminderDispatch",
    "get_messaging_provider",
]
