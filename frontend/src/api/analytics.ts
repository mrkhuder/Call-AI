import { apiClient } from "./client";

export interface NoShowScore {
  appointment_id: string;
  risk_score: number;
  risk_tier: string;
  top_factors: string[];
}

export interface DemandForecast {
  specialty: string;
  date: string;
  expected_demand: number;
  confidence_interval: [number, number];
}

export const fetchNoShowScore = async (appointmentId: string) => {
  const { data } = await apiClient.get<NoShowScore>(`/analytics/no-show/${appointmentId}`);
  return data;
};

export const fetchDemandForecast = async (specialty: string, horizonDays = 7) => {
  const { data } = await apiClient.get<DemandForecast[]>("/analytics/demand", {
    params: { specialty, horizon_days: horizonDays },
  });
  return data;
};
