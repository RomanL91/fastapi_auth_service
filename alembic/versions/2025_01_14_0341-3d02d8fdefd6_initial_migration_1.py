"""Initial migration 1

Revision ID: 3d02d8fdefd6
Revises: 
Create Date: 2025-01-14 03:41:45.288585

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3d02d8fdefd6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("avatar_path", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("last_login", sa.DateTime(), nullable=True),
        sa.Column("external_id", sa.String(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("external_id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=True)
    op.create_table(
        "clientuuids",
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.Column("client_uuid", sa.String(), nullable=False),
        sa.Column("ip_address", sa.String(), nullable=True),
        sa.Column("device_type", sa.String(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("client_uuid"),
    )
    op.create_index(
        op.f("ix_clientuuids_id"), "clientuuids", ["id"], unique=True
    )
    op.create_table(
        "jwtokens",
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.Column("issued_at", sa.DateTime(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column(
            "token_type",
            sa.Enum("ACCESS", "REFRESH", name="tokentypeenum"),
            nullable=False,
        ),
        sa.Column("token", sa.String(length=200), nullable=False),
        sa.Column("revoked", sa.Boolean(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_jwtokens_id"), "jwtokens", ["id"], unique=True)
    op.create_table(
        "phonenumbers",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("phone_number", sa.String(), nullable=False),
        sa.Column("verified_at", sa.DateTime(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("phone_number"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index(
        op.f("ix_phonenumbers_id"), "phonenumbers", ["id"], unique=True
    )
    op.create_table(
        "smscodes",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("code", sa.String(length=6), nullable=False),
        sa.Column(
            "expires_at",
            sa.DateTime(),
            server_default=sa.text("NOW() + INTERVAL '5 MINUTE'"),
            nullable=False,
        ),
        sa.Column("is_used", sa.Boolean(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_smscodes_id"), "smscodes", ["id"], unique=True)
    op.create_table(
        "socialaccounts",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("provider", sa.String(), nullable=False),
        sa.Column("provider_id", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.Column("avatar_url", sa.String(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("provider_id"),
    )
    op.create_index(
        op.f("ix_socialaccounts_id"), "socialaccounts", ["id"], unique=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_socialaccounts_id"), table_name="socialaccounts")
    op.drop_table("socialaccounts")
    op.drop_index(op.f("ix_smscodes_id"), table_name="smscodes")
    op.drop_table("smscodes")
    op.drop_index(op.f("ix_phonenumbers_id"), table_name="phonenumbers")
    op.drop_table("phonenumbers")
    op.drop_index(op.f("ix_jwtokens_id"), table_name="jwtokens")
    op.drop_table("jwtokens")
    op.drop_index(op.f("ix_clientuuids_id"), table_name="clientuuids")
    op.drop_table("clientuuids")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###
