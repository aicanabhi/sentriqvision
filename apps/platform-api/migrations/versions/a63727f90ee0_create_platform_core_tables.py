"""create platform core tables

Revision ID: a63727f90ee0
Revises:
Create Date: 2026-08-13
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# Alembic revision identifiers
revision: str = "a63727f90ee0"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Create the initial platform database schema.

    Hierarchy:

        Organization
            ↓
          Site
            ↓
          Zone
            ↓
         Camera
            ↓
      CameraModule
            ↓
      ModuleConfig

        CameraModule → Module
    """

    # ---------------------------------------------------------
    # 1. Create application schema
    # ---------------------------------------------------------

    op.execute("CREATE SCHEMA IF NOT EXISTS platform")

    # ---------------------------------------------------------
    # 2. Organizations
    # ---------------------------------------------------------

    op.create_table(
        "organizations",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=225),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="platform",
    )

    # ---------------------------------------------------------
    # 3. Sites
    # ---------------------------------------------------------

    op.create_table(
        "sites",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "organization_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "timezone",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["platform.organizations.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="platform",
    )

    # This index exists because organization_id has index=True
    # in the SQLAlchemy Site model.
    op.create_index(
        "ix_platform_sites_organization_id",
        "sites",
        ["organization_id"],
        unique=False,
        schema="platform",
    )

    # ---------------------------------------------------------
    # 4. Zones
    # ---------------------------------------------------------

    op.create_table(
        "zones",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "site_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "zone_type",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["site_id"],
            ["platform.sites.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="platform",
    )

    op.create_index(
        "ix_platform_zones_site_id",
        "zones",
        ["site_id"],
        unique=False,
        schema="platform",
    )

    # ---------------------------------------------------------
    # 5. Cameras
    # ---------------------------------------------------------

    op.create_table(
        "cameras",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "site_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "zone_id",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),
        sa.Column(
            "camera_code",
            sa.String(length=20),
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "rtsp_url",
            sa.String(length=1000),
            nullable=False,
        ),
        sa.Column(
            "resolution",
            sa.String(length=20),
            nullable=False,
        ),
        sa.Column(
            "fps",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["site_id"],
            ["platform.sites.id"],
        ),
        sa.ForeignKeyConstraint(
            ["zone_id"],
            ["platform.zones.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("camera_code", name="uq_cameras_camera_code",),
        schema="platform",
    )

    op.create_index(
        "ix_platform_cameras_site_id",
        "cameras",
        ["site_id"],
        unique=False,
        schema="platform",
    )

    op.create_index(
        "ix_platform_cameras_zone_id",
        "cameras",
        ["zone_id"],
        unique=False,
        schema="platform",
    )

    # ---------------------------------------------------------
    # 6. Modules
    # ---------------------------------------------------------

    op.create_table(
        "modules",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "code",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.String(length=1000),
            nullable=True,
        ),
        sa.Column(
            "enabled",
            sa.Boolean(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code", name="uq_modules_code"),
        schema="platform",
    )

    # ---------------------------------------------------------
    # 7. Camera ↔ Module mapping
    # ---------------------------------------------------------

    op.create_table(
        "camera_modules",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "camera_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "module_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "enabled",
            sa.Boolean(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["camera_id"],
            ["platform.cameras.id"],
        ),
        sa.ForeignKeyConstraint(
            ["module_id"],
            ["platform.modules.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "camera_id",
            "module_id",
            name="uq_camera_module",
        ),
        schema="platform",
    )

    op.create_index(
        "ix_platform_camera_modules_camera_id",
        "camera_modules",
        ["camera_id"],
        unique=False,
        schema="platform",
    )

    op.create_index(
        "ix_platform_camera_modules_module_id",
        "camera_modules",
        ["module_id"],
        unique=False,
        schema="platform",
    )

    # ---------------------------------------------------------
    # 8. Module configuration
    # ---------------------------------------------------------

    op.create_table(
        "module_configs",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "camera_module_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "configuration",
            postgresql.JSON(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["camera_module_id"],
            ["platform.camera_modules.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("camera_module_id", name="uq_module_config_camera_module",),
        schema="platform",
    )

# ---------------------------------------------------------
# Downgrade
# ---------------------------------------------------------

def downgrade() -> None:
    """
    Remove all platform tables and the platform schema.
    """

    # Drop in reverse dependency order.

    op.drop_table(
        "module_configs",
        schema="platform",
    )

    op.drop_index(
        "ix_platform_camera_modules_module_id",
        table_name="camera_modules",
        schema="platform",
    )

    op.drop_index(
        "ix_platform_camera_modules_camera_id",
        table_name="camera_modules",
        schema="platform",
    )

    op.drop_table(
        "camera_modules",
        schema="platform",
    )

    op.drop_table(
        "modules",
        schema="platform",
    )

    op.drop_index(
        "ix_platform_cameras_zone_id",
        table_name="cameras",
        schema="platform",
    )

    op.drop_index(
        "ix_platform_cameras_site_id",
        table_name="cameras",
        schema="platform",
    )

    op.drop_table(
        "cameras",
        schema="platform",
    )

    op.drop_index(
        "ix_platform_zones_site_id",
        table_name="zones",
        schema="platform",
    )

    op.drop_table(
        "zones",
        schema="platform",
    )

    op.drop_index(
        "ix_platform_sites_organization_id",
        table_name="sites",
        schema="platform",
    )

    op.drop_table(
        "sites",
        schema="platform",
    )

    op.drop_table(
        "organizations",
        schema="platform",
    )

    # Finally remove the schema.
    op.execute("DROP SCHEMA IF EXISTS platform")