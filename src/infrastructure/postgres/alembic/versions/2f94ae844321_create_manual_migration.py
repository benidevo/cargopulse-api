"""Create manual migration

Revision ID: 2f94ae844321
Revises:
Create Date: 2024-04-14 12:55:14.400020

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2f94ae844321"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Creating the 'users' table
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("email", sa.String(length=30), nullable=False, unique=True),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("organization", sa.String(length=20), nullable=False),
        sa.Column("industry", sa.String(length=20), nullable=False),
        sa.Column("address", sa.String(length=100), nullable=False),
        sa.Column("state", sa.String(length=10), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Creating the 'api_keys' table
    op.create_table(
        "api_keys",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("api_key", sa.String(length=200), nullable=False, unique=True),
        sa.Column("webhook_url", sa.String(length=200), nullable=False),
        sa.Column(
            "user_id", sa.UUID(), sa.ForeignKey("users.id"), nullable=False, unique=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Creating the 'shipments' table
    op.create_table(
        "shipments",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("tracking_id", sa.String(length=30), nullable=False, unique=True),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("origin_state", sa.String(length=30), nullable=False),
        sa.Column("origin_address", sa.String(length=200), nullable=False),
        sa.Column("destination_state", sa.String(length=30), nullable=False),
        sa.Column("destination_address", sa.String(length=200), nullable=False),
        sa.Column("receiver", sa.String(length=30), nullable=False),
        sa.Column("receiver_contact", sa.String(length=30), nullable=False),
        sa.Column("weight_kg", sa.Numeric(10, 2), nullable=False),
        sa.Column("description", sa.String(length=200), nullable=False),
        sa.Column("value", sa.Numeric(10, 2), nullable=False),
        sa.Column("delivery_instructions", sa.String(length=200), nullable=False),
        sa.Column("events", sa.JSON()),
        sa.Column("user_id", sa.UUID(), sa.ForeignKey("users.id"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    # Dropping the 'shipments' table
    op.drop_table("shipments")

    # Dropping the 'api_keys' table
    op.drop_table("api_keys")

    # Dropping the 'users' table
    op.drop_table("users")
