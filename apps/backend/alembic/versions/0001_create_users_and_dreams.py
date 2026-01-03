"""create users and dreams tables

Revision ID: 0001_create_users_and_dreams
Revises: 
Create Date: 2026-01-02
"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

# revision identifiers, used by Alembic.
revision = '0001_create_users_and_dreams'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('email', sa.String(320), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )

    op.create_table(
        'dreams',
        sa.Column('dream_id', pg.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('timestamp_ingested', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('timestamp_experience', sa.DateTime(timezone=True), nullable=True),
        sa.Column('input_modality', sa.String(), nullable=False),
        sa.Column('content_raw', sa.Text(), nullable=False),
        sa.Column('biometric_context', pg.JSONB(), nullable=True),
        sa.Column('archetype_id', sa.String(), nullable=True),
    )


def downgrade():
    op.drop_table('dreams')
    op.drop_table('users')

# Verification Log
# - Initial migration creates users and dreams tables with UUID PKs and JSONB biometric context.
# - Uses gen_random_uuid() for server-side UUIDs; ensure pgcrypto extension is enabled in DB (CREATE EXTENSION pgcrypto;)
