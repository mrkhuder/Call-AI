import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";

import { AppointmentSuggestion, AppointmentSuggestionQuery, fetchSuggestions } from "../api/appointments";

interface SuggestionPanelProps {
  onSuggestions: (suggestions: AppointmentSuggestion[]) => void;
}

const defaultValues: AppointmentSuggestionQuery = {
  patient_id: "",
  visit_type: "general_consult",
  preferred_days: [],
  location_preferences: [],
};

export function SuggestionPanel({ onSuggestions }: SuggestionPanelProps) {
  const { register, handleSubmit, reset } = useForm<AppointmentSuggestionQuery>({ defaultValues });

  const mutation = useMutation({
    mutationFn: fetchSuggestions,
    onSuccess: (suggestions) => {
      onSuggestions(suggestions);
      reset(defaultValues);
    },
  });

  return (
    <form className="card" onSubmit={handleSubmit((values) => mutation.mutate(values))}>
      <h2>Smart Suggestions</h2>
      <label className="form-label">
        Patient ID
        <input {...register("patient_id", { required: true })} className="input" />
      </label>
      <label className="form-label">
        Visit Type
        <input {...register("visit_type")} className="input" />
      </label>
      <label className="form-label">
        Preferred Days (comma separated)
        <input
          {...register("preferred_days", {
            setValueAs: (value: string) => value.split(",").map((item) => item.trim()).filter(Boolean),
          })}
          className="input"
          placeholder="Tuesday morning, Thursday"
        />
      </label>
      <label className="form-label">
        Location Preferences (comma separated)
        <input
          {...register("location_preferences", {
            setValueAs: (value: string) => value.split(",").map((item) => item.trim()).filter(Boolean),
          })}
          className="input"
          placeholder="clinic-1, telehealth"
        />
      </label>
      <button
        type="submit"
        disabled={mutation.isLoading}
        className="button success"
      >
        {mutation.isLoading ? "Generating..." : "Get Suggestions"}
      </button>
      {mutation.isError && (
        <p className="error-text">
          {(mutation.error as Error)?.message ?? "Unable to fetch suggestions."}
        </p>
      )}
    </form>
  );
}
