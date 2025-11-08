import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";

import { requestNotification, registerWaitlist, WaitlistEntryPayload, WaitlistNotification } from "../api/waitlist";

interface WaitlistCardProps {
  onNotification: (notification: WaitlistNotification) => void;
}

type WaitlistFormState = WaitlistEntryPayload & {
  preferred_locations_text?: string;
  preferred_time_windows_text?: string;
};

const buildDefaults = (): WaitlistFormState => ({
  patient_id: "",
  visit_type: "general_consult",
  preferred_locations_text: "",
  preferred_time_windows_text: "",
  added_at: new Date().toISOString(),
});

export function WaitlistCard({ onNotification }: WaitlistCardProps) {
  const { register, handleSubmit, reset, getValues } = useForm<WaitlistFormState>({
    defaultValues: buildDefaults(),
  });

  const registerMutation = useMutation({
    mutationFn: (payload: WaitlistEntryPayload) => registerWaitlist(payload),
  });

  const notificationMutation = useMutation({
    mutationFn: (payload: WaitlistEntryPayload) => requestNotification(payload),
    onSuccess: (notification) => {
      onNotification(notification);
      reset(buildDefaults());
    },
  });

  const transformPayload = (values: WaitlistFormState): WaitlistEntryPayload => {
    const locationList = (values.preferred_locations_text ?? "")
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean);
    const timeWindows = (values.preferred_time_windows_text ?? "")
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean)
      .map((window) => {
        const [start, end] = window.split("-");
        return [start?.trim() ?? "", end?.trim() ?? ""] as [string, string];
      });

    return {
      patient_id: values.patient_id,
      visit_type: values.visit_type,
      preferred_locations: locationList,
      preferred_time_windows: timeWindows,
      added_at: values.added_at,
    };
  };

  const handleRegister = () => {
    const payload = transformPayload(getValues());
    registerMutation.mutate(payload);
  };

  return (
    <form className="card" onSubmit={handleSubmit((values) => notificationMutation.mutate(transformPayload(values)))}>
      <h2>Waitlist Automation</h2>
      <label className="form-label">
        Patient ID
        <input {...register("patient_id", { required: true })} className="input" />
      </label>
      <label className="form-label">
        Visit Type
        <input {...register("visit_type")} className="input" />
      </label>
      <label className="form-label">
        Preferred Locations (comma separated)
        <input {...register("preferred_locations_text")} className="input" />
      </label>
      <label className="form-label">
        Preferred Time Windows (format HH:MM-HH:MM, comma separated)
        <input
          {...register("preferred_time_windows_text")}
          className="input"
          placeholder="09:00-11:00, 14:00-17:00"
        />
      </label>
      <div className="button-row">
        <button
          type="button"
          onClick={handleRegister}
          disabled={registerMutation.isLoading}
          className="button outline"
        >
          {registerMutation.isLoading ? "Saving..." : "Save Waitlist Profile"}
        </button>
        <button
          type="submit"
          disabled={notificationMutation.isLoading}
          className="button primary"
        >
          {notificationMutation.isLoading ? "Simulating..." : "Simulate Notification"}
        </button>
      </div>
      {(registerMutation.isError || notificationMutation.isError) && (
        <p className="error-text">
          {((registerMutation.error || notificationMutation.error) as Error)?.message ??
            "Waitlist action failed."}
        </p>
      )}
    </form>
  );
}
