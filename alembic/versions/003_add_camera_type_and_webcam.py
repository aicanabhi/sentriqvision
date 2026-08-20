"""add_camera_type_and_webcam

Revision ID: 003_camera_type_webcam
Revises: 002_org_fields
Create Date: 2026-08-20 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '003_camera_type_webcam'
down_revision: Union[str, None] = '002_org_fields'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('cameras', sa.Column('camera_type', sa.String(length=50), nullable=False, server_default='RTSP'))
    op.add_column('cameras', sa.Column('device_index', sa.Integer(), nullable=True))
    op.add_column('cameras', sa.Column('is_running', sa.Boolean(), nullable=False, server_default='false'))


def downgrade() -> None:
    op.drop_column('cameras', 'is_running')
    op.drop_column('cameras', 'device_index')
    op.drop_column('cameras', 'camera_type')
