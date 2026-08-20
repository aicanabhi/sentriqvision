"""create_ai_capability_entitlement_system

Revision ID: 001_ai_capabilities
Revises: 
Create Date: 2026-08-18 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sqla
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_ai_capabilities'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create ai_parameter_catalog
    op.create_table(
        'ai_parameter_catalog',
        sqla.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sqla.Column('service_number', sqla.Integer(), nullable=False, unique=True),
        sqla.Column('code', sqla.String(length=100), nullable=False, unique=True),
        sqla.Column('name', sqla.String(length=255), nullable=False),
        sqla.Column('domain', sqla.String(length=100), nullable=False),
        sqla.Column('description', sqla.Text(), nullable=False),
        sqla.Column('hardware_requirement', sqla.String(length=50), nullable=False),
        sqla.Column('processing_mode', sqla.String(length=50), nullable=False),
        sqla.Column('default_confidence', sqla.Float(), nullable=False, server_default='0.70'),
        sqla.Column('default_fps', sqla.Float(), nullable=False, server_default='10.0'),
        sqla.Column('configuration_schema', postgresql.JSONB(), nullable=False, server_default='{}'),
        sqla.Column('is_active', sqla.Boolean(), nullable=False, server_default='true'),
        sqla.Column('created_at', sqla.DateTime(timezone=True), nullable=False),
        sqla.Column('updated_at', sqla.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_ai_param_cat_service_number', 'ai_parameter_catalog', ['service_number'])
    op.create_index('ix_ai_param_cat_code', 'ai_parameter_catalog', ['code'])
    op.create_index('ix_ai_param_cat_domain', 'ai_parameter_catalog', ['domain'])

    # 2. Create organization_ai_parameters
    op.create_table(
        'organization_ai_parameters',
        sqla.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sqla.Column('organization_id', postgresql.UUID(as_uuid=True), sqla.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False),
        sqla.Column('parameter_id', postgresql.UUID(as_uuid=True), sqla.ForeignKey('ai_parameter_catalog.id', ondelete='RESTRICT'), nullable=False),
        sqla.Column('enabled', sqla.Boolean(), nullable=False, server_default='false'),
        sqla.Column('entitled', sqla.Boolean(), nullable=False, server_default='true'),
        sqla.Column('configured', sqla.Boolean(), nullable=False, server_default='false'),
        sqla.Column('confidence_threshold', sqla.Float(), nullable=False, server_default='0.70'),
        sqla.Column('sampling_fps', sqla.Float(), nullable=False, server_default='10.0'),
        sqla.Column('processing_mode', sqla.String(length=50), nullable=False),
        sqla.Column('device_preference', sqla.String(length=50), nullable=False),
        sqla.Column('alert_enabled', sqla.Boolean(), nullable=False, server_default='true'),
        sqla.Column('retention_days', sqla.Integer(), nullable=False, server_default='30'),
        sqla.Column('configuration_json', postgresql.JSONB(), nullable=False, server_default='{}'),
        sqla.Column('created_at', sqla.DateTime(timezone=True), nullable=False),
        sqla.Column('updated_at', sqla.DateTime(timezone=True), nullable=False),
        sqla.UniqueConstraint('organization_id', 'parameter_id', name='uq_org_parameter'),
    )
    op.create_index('ix_org_ai_param_org_id', 'organization_ai_parameters', ['organization_id'])
    op.create_index('ix_org_ai_param_param_id', 'organization_ai_parameters', ['parameter_id'])
    op.create_index('ix_org_ai_param_org_enabled', 'organization_ai_parameters', ['organization_id', 'enabled'])

    # 3. Create parameter_camera_assignments
    op.create_table(
        'parameter_camera_assignments',
        sqla.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sqla.Column('organization_id', postgresql.UUID(as_uuid=True), sqla.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False),
        sqla.Column('parameter_id', postgresql.UUID(as_uuid=True), sqla.ForeignKey('ai_parameter_catalog.id', ondelete='CASCADE'), nullable=False),
        sqla.Column('camera_id', postgresql.UUID(as_uuid=True), sqla.ForeignKey('cameras.id', ondelete='CASCADE'), nullable=False),
        sqla.Column('enabled', sqla.Boolean(), nullable=False, server_default='true'),
        sqla.Column('created_at', sqla.DateTime(timezone=True), nullable=False),
        sqla.Column('updated_at', sqla.DateTime(timezone=True), nullable=False),
        sqla.UniqueConstraint('organization_id', 'parameter_id', 'camera_id', name='uq_param_cam_assignment'),
    )
    op.create_index('ix_param_cam_assign_org', 'parameter_camera_assignments', ['organization_id'])
    op.create_index('ix_param_cam_assign_param', 'parameter_camera_assignments', ['parameter_id'])
    op.create_index('ix_param_cam_assign_cam', 'parameter_camera_assignments', ['camera_id'])


def downgrade() -> None:
    op.drop_table('parameter_camera_assignments')
    op.drop_table('organization_ai_parameters')
    op.drop_table('ai_parameter_catalog')
