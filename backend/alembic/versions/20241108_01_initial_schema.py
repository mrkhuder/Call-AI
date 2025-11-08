"""initial schema for appointments, reminders, waitlist"""
from alembic import op
import sqlalchemy as sa


revision = "20241108_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "appointment",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("patient_id", sa.String(), nullable=False),
        sa.Column("provider_id", sa.String(), nullable=False),
        sa.Column("reason_for_visit", sa.String(), nullable=False),
        sa.Column("appointment_start", sa.DateTime(), nullable=False),
        sa.Column("appointment_end", sa.DateTime(), nullable=False),
        sa.Column("channel", sa.String(), nullable=False),
        sa.Column("insurance_plan", sa.String(), nullable=True),
        sa.Column("location_id", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=False, server_default="pending"),
        sa.Column("no_show_risk", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_appointment_id", "appointment", ["id"], unique=False)
    op.create_index("ix_appointment_patient_id", "appointment", ["patient_id"], unique=False)
    op.create_index("ix_appointment_provider_id", "appointment", ["provider_id"], unique=False)
    op.create_index("ix_appointment_status", "appointment", ["status"], unique=False)

    op.create_table(
        "reminder",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("appointment_id", sa.String(), nullable=False),
        sa.Column("patient_id", sa.String(), nullable=False),
        sa.Column("channel", sa.String(), nullable=False),
        sa.Column("send_at", sa.DateTime(), nullable=False),
        sa.Column("template_id", sa.String(), nullable=False),
        sa.Column("high_risk", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("additional_context", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=False, server_default="scheduled"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_reminder_id", "reminder", ["id"], unique=False)
    op.create_index("ix_reminder_appointment_id", "reminder", ["appointment_id"], unique=False)
    op.create_index("ix_reminder_channel", "reminder", ["channel"], unique=False)
    op.create_index("ix_reminder_patient_id", "reminder", ["patient_id"], unique=False)

    op.create_table(
        "waitlist",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("patient_id", sa.String(), nullable=False),
        sa.Column("visit_type", sa.String(), nullable=False),
        sa.Column("preferred_locations", sa.String(), nullable=True),
        sa.Column("preferred_time_windows", sa.String(), nullable=True),
        sa.Column("risk_score", sa.Float(), nullable=True),
        sa.Column("added_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_waitlist_id", "waitlist", ["id"], unique=False)
    op.create_index("ix_waitlist_patient_id", "waitlist", ["patient_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_waitlist_patient_id", table_name="waitlist")
    op.drop_index("ix_waitlist_id", table_name="waitlist")
    op.drop_table("waitlist")

    op.drop_index("ix_reminder_patient_id", table_name="reminder")
    op.drop_index("ix_reminder_channel", table_name="reminder")
    op.drop_index("ix_reminder_appointment_id", table_name="reminder")
    op.drop_index("ix_reminder_id", table_name="reminder")
    op.drop_table("reminder")

    op.drop_index("ix_appointment_status", table_name="appointment")
    op.drop_index("ix_appointment_provider_id", table_name="appointment")
    op.drop_index("ix_appointment_patient_id", table_name="appointment")
    op.drop_index("ix_appointment_id", table_name="appointment")
    op.drop_table("appointment")
