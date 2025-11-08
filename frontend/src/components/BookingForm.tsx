import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import dayjs from "dayjs";

import {
  AppointmentRequestPayload,
  AppointmentResponsePayload,
  createAppointment,
} from "../api/appointments";

interface BookingFormProps {
  onSuccess: (response: AppointmentResponsePayload) => void;
}

type BookingFormState = AppointmentRequestPayload;

const buildDefaults = (): BookingFormState => ({
  patient_id: "",
  provider_id: "",
  reason_for_visit: "",
  appointment_start: dayjs().add(2, "day").hour(9).minute(0).second(0).millisecond(0).format("YYYY-MM-DDTHH:mm"),
  appointment_end: dayjs().add(2, "day").hour(9).minute(30).second(0).millisecond(0).format("YYYY-MM-DDTHH:mm"),
  channel: "mobile",
  insurance_plan: "",
  location_id: "",
});

export function BookingForm({ onSuccess }: BookingFormProps) {
  const { register, handleSubmit, reset } = useForm<BookingFormState>({ defaultValues: buildDefaults() });

  const mutation = useMutation({
    mutationFn: createAppointment,
    onSuccess: (response) => {
      onSuccess(response);
      reset(buildDefaults());
    },
  });

  return (
    <form className="card" onSubmit={handleSubmit((values) => mutation.mutate(values))}>
      <h2>Book an Appointment</h2>
      <label className="form-label">
        Patient ID
        <input {...register("patient_id", { required: true })} className="input" />
      </label>
      <label className="form-label">
        Provider ID
        <input {...register("provider_id", { required: true })} className="input" />
      </label>
      <label className="form-label">
        Visit Reason
        <input {...register("reason_for_visit", { required: true })} className="input" />
      </label>
      <label className="form-label">
        Start Time
        <input type="datetime-local" {...register("appointment_start", { required: true })} className="input" />
      </label>
      <label className="form-label">
        End Time
        <input type="datetime-local" {...register("appointment_end", { required: true })} className="input" />
      </label>
      <label className="form-label">
        Channel
        <select {...register("channel")} className="select">
          <option value="mobile">Mobile</option>
          <option value="web">Web</option>
          <option value="phone">Phone</option>
        </select>
      </label>
      <div className="section-grid" style={{ gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))" }}>
        <label className="form-label">
          Insurance Plan
          <input {...register("insurance_plan")} className="input" />
        </label>
        <label className="form-label">
          Location ID
          <input {...register("location_id")} className="input" />
        </label>
      </div>
      <button
        type="submit"
        disabled={mutation.isLoading}
        className="button primary"
      >
        {mutation.isLoading ? "Scheduling..." : "Book Now"}
      </button>
      {mutation.isError && (
        <p className="error-text">
          {(mutation.error as Error)?.message ?? "Unable to schedule appointment."}
        </p>
      )}
    </form>
  );
}
