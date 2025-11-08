import { apiClient } from "./client";

export interface WaitlistEntryPayload {
  patient_id: string;
  visit_type: string;
  preferred_locations?: string[];
  preferred_time_windows?: [string, string][];
  risk_score?: number;
  added_at: string;
}

export interface WaitlistRegisterResponse {
  waitlist_id: string;
}

export interface WaitlistNotification {
  slot_start: string;
  slot_end: string;
  location_id: string;
  expires_at: string;
  message: string;
}

export const registerWaitlist = async (payload: WaitlistEntryPayload) => {
  const { data } = await apiClient.post<WaitlistRegisterResponse>("/waitlist", payload);
  return data;
};

export const requestNotification = async (payload: WaitlistEntryPayload) => {
  const { data } = await apiClient.post<WaitlistNotification>("/waitlist/notify", payload);
  return data;
};
