import { useState } from "react";

import "./App.css";

import { AppointmentResponsePayload, AppointmentSuggestion } from "./api/appointments";
import { NoShowScore } from "./api/analytics";
import { WaitlistNotification } from "./api/waitlist";
import { BookingForm } from "./components/BookingForm";
import { NoShowRiskCard } from "./components/NoShowRiskCard";
import { SuggestionPanel } from "./components/SuggestionPanel";
import { WaitlistCard } from "./components/WaitlistCard";

function App() {
  const [appointmentConfirmation, setAppointmentConfirmation] = useState<AppointmentResponsePayload | null>(null);
  const [suggestions, setSuggestions] = useState<AppointmentSuggestion[]>([]);
  const [riskScore, setRiskScore] = useState<NoShowScore | null>(null);
  const [waitlistNotification, setWaitlistNotification] = useState<WaitlistNotification | null>(null);

  return (
    <div className="app-shell">
      <header className="hero">
        <h1>CareFlow AI</h1>
        <p>
          Predictive scheduling and proactive engagement for healthcare systems. Reduce no-shows, unlock capacity, and
          deliver a frictionless patient experience across mobile, web, and phone channels.
        </p>
      </header>

      <section className="section-grid">
        <BookingForm onSuccess={setAppointmentConfirmation} />
        <SuggestionPanel onSuggestions={setSuggestions} />
        <NoShowRiskCard onScore={setRiskScore} />
        <WaitlistCard onNotification={setWaitlistNotification} />
      </section>

      <section className="results-panel" style={{ marginTop: "2.5rem" }}>
        {appointmentConfirmation && (
          <div className="suggestion-list">
            <h3>Latest Appointment</h3>
            <div className="suggestion-item">
              <div className={`badge status-${appointmentConfirmation.status}`}>{appointmentConfirmation.status}</div>
              <p className="form-label" style={{ fontWeight: 500, margin: 0 }}>
                Confirmation #{appointmentConfirmation.appointment_id}
              </p>
              {typeof appointmentConfirmation.no_show_risk === "number" && (
                <span className="badge confidence">
                  No-show risk: {(appointmentConfirmation.no_show_risk * 100).toFixed(1)}%
                </span>
              )}
              {appointmentConfirmation.message && <p style={{ margin: 0 }}>{appointmentConfirmation.message}</p>}
            </div>
          </div>
        )}

        {suggestions.length > 0 && (
          <div className="suggestion-list">
            <h3>Suggested Slots</h3>
            {suggestions.map((suggestion) => (
              <div className="suggestion-item" key={`${suggestion.provider_id}-${suggestion.slot_start}`}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
                  <strong>{new Date(suggestion.slot_start).toLocaleString()}</strong>
                  <span className="badge confidence">{Math.round(suggestion.confidence * 100)}% match</span>
                </div>
                <p style={{ margin: 0 }}>Provider: {suggestion.provider_id}</p>
                <p style={{ margin: 0 }}>Location: {suggestion.location_id}</p>
                {suggestion.personalization_reason && <p style={{ margin: 0 }}>{suggestion.personalization_reason}</p>}
              </div>
            ))}
          </div>
        )}

        {riskScore && (
          <div className="risk-insights">
            <h3>No-Show Risk Insights</h3>
            <div className="risk-score">
              {(riskScore.risk_score * 100).toFixed(1)}%
              <span className={`risk-tier ${riskScore.risk_tier}`}>{riskScore.risk_tier}</span>
            </div>
            <ul className="factor-list">
              {riskScore.top_factors.map((factor) => (
                <li key={factor}>{factor}</li>
              ))}
            </ul>
          </div>
        )}

        {waitlistNotification && (
          <div className="notification-panel">
            <h3>Waitlist Notification</h3>
            <p style={{ margin: 0 }}>{waitlistNotification.message}</p>
            <p style={{ margin: "0.35rem 0 0", fontSize: "0.9rem", color: "#475569" }}>
              Slot: {new Date(waitlistNotification.slot_start).toLocaleString()} -{" "}
              {new Date(waitlistNotification.slot_end).toLocaleString()}
            </p>
            <p style={{ margin: "0.35rem 0 0", fontSize: "0.9rem", color: "#475569" }}>
              Expires at: {new Date(waitlistNotification.expires_at).toLocaleTimeString()}
            </p>
          </div>
        )}
      </section>
    </div>
  );
}

export default App;
