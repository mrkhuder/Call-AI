import { apiClient } from "./client";

export interface ReminderPayload {
  appointment_id: string;
  patient_id: string;
  channel: "sms" | "email" | "push";
  send_at: string;
  template_id: string;
  high_risk?: boolean;
  additional_context?: string;
}

export interface ReminderResponse {
  reminder_id: string;
  status: "scheduled" | "sent" | "error";
  message?: string;
}

export const createReminder = async (payload: ReminderPayload) => {
  const { data } = await apiClient.post<ReminderResponse>("/reminders", payload);
  return data;
};
