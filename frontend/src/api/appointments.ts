import { apiClient } from "./client";

export interface AppointmentRequestPayload {
  patient_id: string;
  provider_id: string;
  reason_for_visit: string;
  appointment_start: string;
  appointment_end: string;
  channel: "mobile" | "web" | "phone";
  insurance_plan?: string;
  location_id?: string;
}

export interface AppointmentResponsePayload {
  appointment_id: string;
  status: "confirmed" | "pending" | "waitlisted";
  no_show_risk?: number;
  message?: string;
}

export interface AppointmentSuggestionQuery {
  patient_id: string;
  preferred_days?: string[];
  preferred_time_window?: [string, string];
  visit_type?: string;
  previous_provider_id?: string;
  location_preferences?: string[];
}

export interface AppointmentSuggestion {
  provider_id: string;
  slot_start: string;
  slot_end: string;
  location_id: string;
  visit_type: string;
  confidence: number;
  personalization_reason?: string;
}

export const createAppointment = async (payload: AppointmentRequestPayload) => {
  const { data } = await apiClient.post<AppointmentResponsePayload>("/scheduling", payload);
  return data;
};

export const fetchSuggestions = async (payload: AppointmentSuggestionQuery) => {
  const { data } = await apiClient.post<AppointmentSuggestion[]>("/scheduling/suggestions", payload);
  return data;
};
