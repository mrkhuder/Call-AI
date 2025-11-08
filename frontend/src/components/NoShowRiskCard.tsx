import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";

import { NoShowScore, fetchNoShowScore } from "../api/analytics";

interface NoShowRiskCardProps {
  onScore: (score: NoShowScore) => void;
}

interface NoShowRiskFormState {
  appointment_id: string;
}

const defaultValues: NoShowRiskFormState = {
  appointment_id: "",
};

export function NoShowRiskCard({ onScore }: NoShowRiskCardProps) {
  const { register, handleSubmit, reset } = useForm<NoShowRiskFormState>({ defaultValues });

  const mutation = useMutation({
    mutationFn: ({ appointment_id }: NoShowRiskFormState) => fetchNoShowScore(appointment_id),
    onSuccess: (score) => {
      onScore(score);
      reset(defaultValues);
    },
  });

  return (
    <form className="card" onSubmit={handleSubmit((values) => mutation.mutate(values))}>
      <h2>No-Show Risk Lookup</h2>
      <label className="form-label">
        Appointment ID
        <input {...register("appointment_id", { required: true })} className="input" />
      </label>
      <button
        type="submit"
        disabled={mutation.isLoading}
        className="button warning"
      >
        {mutation.isLoading ? "Scoring..." : "Get Risk Score"}
      </button>
      {mutation.isError && (
        <p className="error-text">
          {(mutation.error as Error)?.message ?? "Unable to fetch risk score."}
        </p>
      )}
    </form>
  );
}
