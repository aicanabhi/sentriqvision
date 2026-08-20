"""add_organization_fields

Revision ID: 002_org_fields
Revises: 001_ai_capabilities
Create Date: 2026-08-20 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002_org_fields'
down_revision: Union[str, None] = '001_ai_capabilities'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('organizations', sa.Column('status', sa.String(length=50), nullable=False, server_default='ACTIVE'))
    op.add_column('organizations', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('organizations', sa.Column('contact_email', sa.String(length=255), nullable=True))
    op.add_column('organizations', sa.Column('address', sa.String(length=255), nullable=True))
    op.add_column('organizations', sa.Column('timezone', sa.String(length=100), nullable=False, server_default='UTC'))
    op.add_column('organizations', sa.Column('subscription_tier', sa.String(length=100), nullable=False, server_default='ENTERPRISE'))


def downgrade() -> None:
    op.drop_column('organizations', 'subscription_tier')
    op.drop_column('organizations', 'timezone')
    op.drop_column('organizations', 'address')
    op.drop_column('organizations', 'contact_email')
    op.drop_column('organizations', 'deleted_at')
    op.drop_column('organizations', 'status')
