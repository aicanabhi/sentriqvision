import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.logging import logger
from app.models.organization import Organization
from app.models.ai_parameter import (
    AIInferenceLog,
    AIParameterCatalog,
    AuditLog,
    OrganizationAIParameter,
    ParameterCameraAssignment,
)


# ============================================================
# CANONICAL 54 AI CAPABILITIES
# ============================================================

CANONICAL_54_SERVICES = [
    (
        1,
        "FACE_DETECTION",
        "Face Detection",
        "Face & Identity",
        "Detects face bounding boxes and facial landmark points.",
        "GPU",
        "Real-time",
    ),
    (
        2,
        "FACE_RECOGNITION",
        "Face Recognition",
        "Face & Identity",
        "512d vector embedding matching using ArcFace and pgvector.",
        "GPU",
        "Real-time",
    ),
    (
        3,
        "FACE_LIVENESS",
        "Face Liveness",
        "Face & Identity",
        "Anti-spoofing liveness detection against 2D photos and screens.",
        "GPU",
        "Real-time",
    ),
    (
        4,
        "FACE_QUALITY_ANALYSIS",
        "Face Quality Analysis",
        "Face & Identity",
        "Evaluates sharpness, head pose pitch/yaw, and illumination quality.",
        "GPU",
        "Real-time",
    ),
    (
        5,
        "FACE_TRACKING",
        "Face Tracking",
        "Face & Identity",
        "Assigns persistent IDs to facial tracks across video frames.",
        "GPU",
        "Real-time",
    ),
    (
        6,
        "PERSON_DETECTION",
        "Person Detection",
        "People & Behavior",
        "Detects human bodies in indoor and outdoor surveillance feeds.",
        "GPU",
        "Real-time",
    ),
    (
        7,
        "PERSON_TRACKING",
        "Person Tracking",
        "People & Behavior",
        "Tracks person trajectories and spatial movement over time.",
        "GPU",
        "Real-time",
    ),
    (
        8,
        "CROWD_DETECTION",
        "Crowd Detection",
        "People & Behavior",
        "Measures crowd density and detects dangerous crowding levels.",
        "GPU",
        "Real-time",
    ),
    (
        9,
        "LOITERING_DETECTION",
        "Loitering Detection",
        "People & Behavior",
        "Flags individuals staying in designated zones past threshold duration.",
        "GPU",
        "Real-time",
    ),
    (
        10,
        "INTRUSION_DETECTION",
        "Intrusion Detection",
        "Security & Access",
        "Triggers alerts when humans/vehicles breach defined security polygons.",
        "GPU",
        "Real-time",
    ),
    (
        11,
        "RESTRICTED_ZONE_DETECTION",
        "Restricted Zone Detection",
        "Security & Access",
        "Monitors secure perimeters and confidential areas for unauthorized entry.",
        "GPU",
        "Real-time",
    ),
    (
        12,
        "LINE_CROSSING_DETECTION",
        "Line Crossing Detection",
        "Security & Access",
        "Detects directional crossing across virtual tripwire lines.",
        "GPU",
        "Real-time",
    ),
    (
        13,
        "DWELL_TIME_DETECTION",
        "Dwell Time Detection",
        "Analytics & Insights",
        "Calculates total time subjects remain within specific retail/security areas.",
        "GPU",
        "Real-time",
    ),
    (
        14,
        "FALL_DETECTION",
        "Fall Detection",
        "Safety & Health",
        "Detects sudden human falls and unresponsiveness for emergency dispatch.",
        "GPU",
        "Real-time",
    ),
    (
        15,
        "FIGHT_DETECTION",
        "Fight Detection",
        "Security & Access",
        "Monitors physical altercations, rapid violent gestures, and brawls.",
        "GPU",
        "Real-time",
    ),
    (
        16,
        "VIOLENCE_DETECTION",
        "Violence Detection",
        "Security & Access",
        "AI model detecting physical aggression and violent interactions.",
        "GPU",
        "Real-time",
    ),
    (
        17,
        "ABANDONED_OBJECT_DETECTION",
        "Abandoned Object Detection",
        "Security & Access",
        "Flags stationary unattended baggage, packages, or suspicious items.",
        "GPU",
        "Real-time",
    ),
    (
        18,
        "LEFT_OBJECT_DETECTION",
        "Left Object Detection",
        "Security & Access",
        "Detects objects placed and left behind in public transit/spaces.",
        "GPU",
        "Real-time",
    ),
    (
        19,
        "WRONG_DIRECTION_DETECTION",
        "Wrong Direction Detection",
        "Transportation",
        "Detects vehicles or pedestrians moving counter to designated flow.",
        "GPU",
        "Real-time",
    ),
    (
        20,
        "PPE_HELMET_DETECTION",
        "PPE Helmet Detection",
        "Safety & Health",
        "Verifies hardhat compliance on construction and industrial sites.",
        "GPU",
        "Real-time",
    ),
    (
        21,
        "PPE_SAFETY_VEST_DETECTION",
        "PPE Safety Vest Detection",
        "Safety & Health",
        "Verifies high-visibility safety vest compliance.",
        "GPU",
        "Real-time",
    ),
    (
        22,
        "PPE_MASK_DETECTION",
        "PPE Mask Detection",
        "Safety & Health",
        "Detects facial mask and respirator compliance.",
        "GPU",
        "Real-time",
    ),
    (
        23,
        "SMOKE_DETECTION",
        "Smoke Detection",
        "Safety & Health",
        "Early optical detection of rising smoke plumes.",
        "GPU",
        "Real-time",
    ),
    (
        24,
        "FIRE_DETECTION",
        "Fire Detection",
        "Safety & Health",
        "Optical and thermal flame detection for fire hazard alerting.",
        "GPU",
        "Real-time",
    ),
    (
        25,
        "GLASS_BREAK_DETECTION",
        "Glass Break Detection",
        "Security & Access",
        "Visual and acoustic glass shatter and forced entry detection.",
        "GPU",
        "Real-time",
    ),
    (
        26,
        "VEHICLE_DETECTION",
        "Vehicle Detection",
        "Transportation",
        "Detects automobiles, trucks, buses, motorcycles, and bicycles.",
        "GPU",
        "Real-time",
    ),
    (
        27,
        "VEHICLE_TRACKING",
        "Vehicle Tracking",
        "Transportation",
        "Multi-camera vehicle trajectory tracking and speed estimation.",
        "GPU",
        "Real-time",
    ),
    (
        28,
        "ANPR_LPR",
        "ANPR / LPR",
        "Transportation",
        "Automatic Number Plate Recognition with region format matching.",
        "GPU",
        "Real-time",
    ),
    (
        29,
        "LICENSE_PLATE_OCR",
        "License Plate OCR",
        "Transportation",
        "High-accuracy optical character recognition for license plates.",
        "GPU",
        "Real-time",
    ),
    (
        30,
        "VEHICLE_COLOR_CLASSIFICATION",
        "Vehicle Color Classification",
        "Transportation",
        "Classifies primary and secondary vehicle paint colors.",
        "GPU",
        "Real-time",
    ),
    (
        31,
        "VEHICLE_TYPE_CLASSIFICATION",
        "Vehicle Type Classification",
        "Transportation",
        "Classifies vehicle body types (Sedan, SUV, Pickup, Van, Truck).",
        "GPU",
        "Real-time",
    ),
    (
        32,
        "VEHICLE_MAKE_MODEL_CLASSIFICATION",
        "Vehicle Make/Model Classification",
        "Transportation",
        "Identifies vehicle manufacturer make and model series.",
        "GPU",
        "Real-time",
    ),
    (
        33,
        "SEATBELT_DETECTION",
        "Seatbelt Detection",
        "Safety & Health",
        "Detects driver and passenger seatbelt compliance inside vehicles.",
        "GPU",
        "Real-time",
    ),
    (
        34,
        "WRONG_PARKING_DETECTION",
        "Wrong Parking Detection",
        "Transportation",
        "Detects illegal parking, blocked emergency lanes, and double parking.",
        "GPU",
        "Real-time",
    ),
    (
        35,
        "PARKING_OCCUPANCY",
        "Parking Occupancy",
        "Transportation",
        "Monitors open vs occupied parking stall availability in real time.",
        "GPU",
        "Real-time",
    ),
    (
        36,
        "VEHICLE_SPEED_ESTIMATION",
        "Vehicle Speed Estimation",
        "Transportation",
        "Calculates vehicle velocity across calibrated camera zones.",
        "GPU",
        "Real-time",
    ),
    (
        37,
        "TRAFFIC_FLOW_ANALYSIS",
        "Traffic Flow Analysis",
        "Transportation",
        "Analyzes traffic volume throughput, congestion, and average speed.",
        "GPU",
        "Real-time",
    ),
    (
        38,
        "OBJECT_COUNTING",
        "Object Counting",
        "Analytics & Insights",
        "Counts target objects crossing virtual lines or inside ROI zones.",
        "GPU",
        "Real-time",
    ),
    (
        39,
        "PEOPLE_COUNTING",
        "People Counting",
        "Analytics & Insights",
        "Real-time footfall counting for entry/exit capacity management.",
        "GPU",
        "Real-time",
    ),
    (
        40,
        "QUEUE_DETECTION",
        "Queue Detection",
        "Analytics & Insights",
        "Detects queue formation at checkout counters and service desks.",
        "GPU",
        "Real-time",
    ),
    (
        41,
        "QUEUE_LENGTH_ANALYSIS",
        "Queue Length Analysis",
        "Analytics & Insights",
        "Measures active queue depth, waiting times, and service bottlenecks.",
        "GPU",
        "Real-time",
    ),
    (
        42,
        "OCCUPANCY_ANALYSIS",
        "Occupancy Analysis",
        "Analytics & Insights",
        "Tracks real-time facility occupancy against maximum safety limits.",
        "GPU",
        "Real-time",
    ),
    (
        43,
        "HEATMAP_ANALYTICS",
        "Heatmap Analytics",
        "Analytics & Insights",
        "Generates spatial movement and foot traffic intensity heatmaps.",
        "GPU",
        "Real-time",
    ),
    (
        44,
        "OCR",
        "General OCR Engine",
        "Analytics & Insights",
        "Extracts printed text from shipping containers, badges, and labels.",
        "GPU",
        "Real-time",
    ),
    (
        45,
        "DOCUMENT_DETECTION",
        "Document Detection",
        "Security & Access",
        "Detects physical ID cards, passports, and driver licenses.",
        "GPU",
        "Real-time",
    ),
    (
        46,
        "CAMERA_TAMPER_DETECTION",
        "Camera Tamper Detection",
        "Device & System",
        "Detects camera spray paint, defocus, tilt, or obstruction.",
        "CPU/GPU",
        "Real-time",
    ),
    (
        47,
        "CAMERA_OFFLINE_DETECTION",
        "Camera Offline Detection",
        "Device & System",
        "Monitors stream loss, RTSP timeouts, and network disconnects.",
        "CPU",
        "Real-time",
    ),
    (
        48,
        "ANOMALY_DETECTION",
        "General Anomaly Detection",
        "Intelligence",
        "Unsupervised AI flagging abnormal visual patterns and behaviors.",
        "GPU",
        "Real-time",
    ),
    (
        49,
        "BEHAVIOR_ANOMALY_DETECTION",
        "Behavior Anomaly Detection",
        "Intelligence",
        "Flags errant human movements, panic running, or erratic behavior.",
        "GPU",
        "Real-time",
    ),
    (
        50,
        "SLIP_TRIP_DETECTION",
        "Slip & Trip Detection",
        "Safety & Health",
        "Detects hazardous slips, trips, and industrial surface falls.",
        "GPU",
        "Real-time",
    ),
    (
        51,
        "ACCESS_CONTROL",
        "Access Control System",
        "Security & Access",
        "Integrates face/ANPR biometrics with physical door relays and gates.",
        "CPU/GPU",
        "Real-time",
    ),
    (
        52,
        "EVENT_CORRELATION",
        "Event Correlation Engine",
        "Intelligence",
        "Correlates multi-camera events into unified incident stories.",
        "CPU",
        "Real-time",
    ),
    (
        53,
        "AI_RULE_ENGINE",
        "AI Rule Engine",
        "Intelligence",
        "Evaluates multi-condition spatial-temporal logic rules for alert dispatch.",
        "CPU",
        "Real-time",
    ),
    (
        54,
        "ALERT_INTELLIGENCE",
        "Alert Intelligence & RAG",
        "Intelligence",
        "LLM-assisted alert summaries, root cause, and dispatch actions.",
        "GPU",
        "Real-time",
    ),
]


class ParameterService:
    """
    Business logic for the 54 AI capability catalog and
    organization-specific entitlement/configuration.

    IMPORTANT ARCHITECTURE:

        AIParameterCatalog
                |
                | global master catalog
                v
        OrganizationAIParameter
                |
                | organization-specific state
                v
        ParameterCameraAssignment

    Super Admin must explicitly grant entitlement to an organization.

    enabled=True is only allowed when entitled=True.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    # ========================================================
    # INTERNAL HELPERS
    # ========================================================

    async def _get_org_parameter(
        self,
        org_id: uuid.UUID,
        param_id: Any,
    ) -> Optional[OrganizationAIParameter]:
        """
        Resolve parameter by either:

        1. catalog parameter_id (UUID)
        2. organization parameter row id (UUID)
        3. catalog code (str)

        Always scoped to the requested organization.
        """
        param_str = str(param_id)
        is_uuid = False
        param_uuid = None
        try:
            param_uuid = uuid.UUID(param_str)
            is_uuid = True
        except ValueError:
            param_uuid = None

        if is_uuid:
            query = (
                select(OrganizationAIParameter)
                .options(selectinload(OrganizationAIParameter.catalog_item))
                .where(
                    OrganizationAIParameter.organization_id == org_id,
                    (
                        (OrganizationAIParameter.parameter_id == param_uuid)
                        | (OrganizationAIParameter.id == param_uuid)
                    ),
                )
            )
        else:
            query = (
                select(OrganizationAIParameter)
                .join(AIParameterCatalog, OrganizationAIParameter.parameter_id == AIParameterCatalog.id)
                .options(selectinload(OrganizationAIParameter.catalog_item))
                .where(
                    OrganizationAIParameter.organization_id == org_id,
                    AIParameterCatalog.code == param_str,
                )
            )

        result = await self.db.execute(query)
        org_param = result.scalar_one_or_none()

        if not org_param:
            cat_query = select(AIParameterCatalog)
            if is_uuid:
                cat_query = cat_query.where(
                    (AIParameterCatalog.id == param_uuid) | (AIParameterCatalog.code == param_str)
                )
            else:
                cat_query = cat_query.where(AIParameterCatalog.code == param_str)
            cat_item = (await self.db.execute(cat_query)).scalar_one_or_none()

            if cat_item:
                org_param = OrganizationAIParameter(
                    organization_id=org_id,
                    parameter_id=cat_item.id,
                    enabled=False,
                    entitled=False,
                    configured=False,
                    confidence_threshold=cat_item.default_confidence,
                    sampling_fps=cat_item.default_fps,
                    processing_mode=cat_item.processing_mode,
                    device_preference="GPU" if cat_item.hardware_requirement == "CPU/GPU" else cat_item.hardware_requirement,
                    alert_enabled=True,
                    retention_days=30,
                    configuration_json={"auto_action": "ALERT", "roi_enabled": False},
                )
                self.db.add(org_param)
                await self.db.flush()
                org_param.catalog_item = cat_item

        return org_param

    # ========================================================
    # CATALOG SEEDING + ORGANIZATION ENTITLEMENTS
    # ========================================================

    async def seed_catalog_and_org_entitlements(
        self,
        org_id: Optional[uuid.UUID] = None,
    ) -> None:
        """
        Ensure:

        - all 54 master capabilities exist
        - organization has one row for every capability
        - new organization capabilities start:
              entitled=False
              enabled=False
              configured=False

        This prevents automatic entitlement assignment.
        """

        logger.info(
            "Synchronizing AI capability catalog (org_id=%s)",
            org_id,
        )

        # ----------------------------------------------------
        # 1. Load existing master catalog
        # ----------------------------------------------------

        catalog_result = await self.db.execute(
            select(AIParameterCatalog)
        )

        existing_catalog = {
            item.code: item
            for item in catalog_result.scalars().all()
        }

        # ----------------------------------------------------
        # 2. Add missing canonical capabilities
        # ----------------------------------------------------

        catalog_to_add: List[AIParameterCatalog] = []

        for (
            service_number,
            code,
            name,
            domain,
            description,
            hardware_requirement,
            processing_mode,
        ) in CANONICAL_54_SERVICES:

            if code in existing_catalog:
                continue

            catalog_item = AIParameterCatalog(
                service_number=service_number,
                code=code,
                name=name,
                domain=domain,
                description=description,
                hardware_requirement=hardware_requirement,
                processing_mode=processing_mode,
                default_confidence=0.70,
                default_fps=10.0,
                configuration_schema={
                    "confidence_slider": True,
                    "sampling_fps": True,
                    "device_select": True,
                    "camera_assignment": True,
                    "alert_policy": True,
                },
                is_active=True,
            )

            self.db.add(catalog_item)
            catalog_to_add.append(catalog_item)

        if catalog_to_add:
            await self.db.flush()

            logger.info(
                "Added %s missing AI capabilities to master catalog",
                len(catalog_to_add),
            )

        # ----------------------------------------------------
        # 3. Reload complete catalog
        # ----------------------------------------------------

        catalog_result = await self.db.execute(
            select(AIParameterCatalog).order_by(
                AIParameterCatalog.service_number
            )
        )

        all_catalog = catalog_result.scalars().all()

        # ----------------------------------------------------
        # 4. Load target organization(s)
        # ----------------------------------------------------
        if org_id is not None:
            target_org_ids = [org_id]
        else:
            orgs_res = await self.db.execute(select(Organization.id))
            target_org_ids = orgs_res.scalars().all()

        for target_id in target_org_ids:
            org_result = await self.db.execute(
                select(OrganizationAIParameter).where(
                    OrganizationAIParameter.organization_id == target_id
                )
            )

            existing_org_params = {
                item.parameter_id: item
                for item in org_result.scalars().all()
            }

            created_count = 0

            for catalog in all_catalog:
                if catalog.id in existing_org_params:
                    continue

                org_parameter = OrganizationAIParameter(
                    organization_id=target_id,
                    parameter_id=catalog.id,

                    enabled=False,
                    entitled=False,
                    configured=False,

                    confidence_threshold=catalog.default_confidence,
                    sampling_fps=catalog.default_fps,
                    processing_mode=catalog.processing_mode,
                    device_preference=(
                        "GPU"
                        if catalog.hardware_requirement == "CPU/GPU"
                        else catalog.hardware_requirement
                    ),
                    alert_enabled=True,
                    retention_days=30,
                    configuration_json={
                        "auto_action": "ALERT",
                        "roi_enabled": False,
                    },
                )

                self.db.add(org_parameter)
                created_count += 1

            if created_count:
                logger.info(
                    "Created %s organization AI capability rows for %s",
                    created_count,
                    target_id,
                )

        await self.db.flush()

        logger.info(
            "AI capabilities synchronized for organization %s",
            org_id,
        )

    # ========================================================
    # GET ORGANIZATION PARAMETERS
    # ========================================================

    async def get_organization_parameters(
        self,
        org_id: uuid.UUID,
        domain: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Return all 54 capabilities with organization-specific state.

        IMPORTANT:

        This method never returns another organization's state.

        Example:

            Organization A -> FACE_DETECTION enabled=True
            Organization B -> FACE_DETECTION enabled=False

        The two states remain completely isolated.
        """

        await self.seed_catalog_and_org_entitlements(org_id)

        query = (
            select(OrganizationAIParameter)
            .options(
                selectinload(
                    OrganizationAIParameter.catalog_item
                )
            )
            .where(
                OrganizationAIParameter.organization_id == org_id
            )
        )

        result = await self.db.execute(query)
        org_params = result.scalars().all()

        # ----------------------------------------------------
        # Camera assignments
        # ----------------------------------------------------

        assignments_result = await self.db.execute(
            select(ParameterCameraAssignment).where(
                ParameterCameraAssignment.organization_id == org_id
            )
        )

        assignments = assignments_result.scalars().all()

        camera_count_map: Dict[uuid.UUID, int] = {}

        for assignment in assignments:

            if not assignment.enabled:
                continue

            camera_count_map[assignment.parameter_id] = (
                camera_count_map.get(
                    assignment.parameter_id,
                    0,
                )
                + 1
            )

        # ----------------------------------------------------
        # Build response
        # ----------------------------------------------------

        output: List[Dict[str, Any]] = []

        for org_parameter in org_params:

            catalog = org_parameter.catalog_item

            if not catalog:
                continue

            # ------------------------------------------------
            # Domain filter
            # ------------------------------------------------

            if domain and domain.lower() != "all":

                if domain.lower() not in catalog.domain.lower():
                    continue

            # ------------------------------------------------
            # Status filter
            # ------------------------------------------------

            if status and status.lower() != "all":

                normalized_status = status.lower()

                if normalized_status == "enabled":
                    if not org_parameter.enabled:
                        continue

                elif normalized_status == "disabled":
                    if org_parameter.enabled:
                        continue

                elif normalized_status == "entitled":
                    if not org_parameter.entitled:
                        continue

                elif normalized_status == "unentitled":
                    if org_parameter.entitled:
                        continue

            # ------------------------------------------------
            # Search filter
            # ------------------------------------------------

            if search:

                search_value = search.lower()

                searchable_text = " ".join(
                    [
                        catalog.name or "",
                        catalog.code or "",
                        catalog.domain or "",
                        catalog.description or "",
                    ]
                ).lower()

                if search_value not in searchable_text:
                    continue

            # ------------------------------------------------
            # Camera count
            # ------------------------------------------------

            active_cameras = (
                camera_count_map.get(catalog.id, 0)
                if org_parameter.enabled
                else 0
            )

            # ------------------------------------------------
            # Output
            # ------------------------------------------------

            output.append(
                {
                    "id": str(org_parameter.id),

                    "parameter_id": str(catalog.id),

                    "service_number": catalog.service_number,

                    "code": catalog.code,

                    "name": catalog.name,

                    "domain": catalog.domain,

                    "description": catalog.description,

                    "hardware_requirement": (
                        catalog.hardware_requirement
                    ),

                    "processing_mode": (
                        org_parameter.processing_mode
                    ),

                    "device_preference": (
                        org_parameter.device_preference
                    ),

                    "status": (
                        "ENABLED"
                        if org_parameter.enabled
                        else "DISABLED"
                    ),

                    "enabled": bool(
                        org_parameter.enabled
                    ),

                    "entitled": bool(
                        org_parameter.entitled
                    ),

                    "configured": bool(
                        org_parameter.configured
                    ),

                    "confidence_threshold": float(
                        org_parameter.confidence_threshold
                    ),

                    "sampling_fps": float(
                        org_parameter.sampling_fps
                    ),

                    "alert_enabled": bool(
                        org_parameter.alert_enabled
                    ),

                    "retention_days": int(
                        org_parameter.retention_days
                    ),

                    "active_cameras": active_cameras,

                    "configuration_json": (
                        org_parameter.configuration_json
                        or {}
                    ),

                    "created_at": (
                        org_parameter.created_at.isoformat()
                        if org_parameter.created_at
                        else None
                    ),

                    "updated_at": (
                        org_parameter.updated_at.isoformat()
                        if org_parameter.updated_at
                        else None
                    ),
                }
            )

        output.sort(
            key=lambda item: item["service_number"]
        )

        return output

    # ========================================================
    # TOGGLE / ENABLE / DISABLE
    # ========================================================

    async def toggle_parameter(
        self,
        org_id: uuid.UUID,
        param_id: Any,
        enabled: bool,
        is_superadmin: bool = False,
    ) -> Dict[str, Any]:
        """
        Enable/disable a capability for ONE organization.
        """

        org_parameter = await self._get_org_parameter(
            org_id=org_id,
            param_id=param_id,
        )

        if not org_parameter:
            raise ValueError(
                f"AI capability entitlement '{param_id}' does not exist for this organization"
            )

        # ----------------------------------------------------
        # Handle entitlement
        # ----------------------------------------------------

        if enabled and not org_parameter.entitled:
            if is_superadmin:
                org_parameter.entitled = True
            else:
                raise ValueError(
                    "AI capability is not entitled for this organization. "
                    "Super Admin must assign the entitlement first."
                )

        # ----------------------------------------------------
        # Update state
        # ----------------------------------------------------

        org_parameter.enabled = bool(enabled)

        org_parameter.updated_at = (
            datetime.now(timezone.utc)
        )

        # ----------------------------------------------------
        # Audit
        # ----------------------------------------------------

        audit = AuditLog(
            organization_id=org_id,
            action="TOGGLE_AI_PARAMETER",
            resource_type="organization_ai_parameter",
            resource_id=str(
                org_parameter.parameter_id
            ),
            details={
                "enabled": bool(enabled),
                "entitled": bool(
                    org_parameter.entitled
                ),
            },
        )

        self.db.add(audit)

        await self.db.commit()

        await self.db.refresh(org_parameter)

        return {
            "success": True,
            "organization_id": str(org_id),
            "parameter_id": str(
                org_parameter.parameter_id
            ),
            "enabled": bool(
                org_parameter.enabled
            ),
            "entitled": bool(
                org_parameter.entitled
            ),
        }

    # ========================================================
    # ASSIGN ENTITLEMENT
    # ========================================================

    async def assign_entitlement(
        self,
        org_id: uuid.UUID,
        param_id: uuid.UUID,
        enabled: bool = False,
    ) -> Dict[str, Any]:
        """
        Super Admin operation.

        Grants/revokes an AI capability entitlement for one
        organization.

        Flow:

            Super Admin
                |
                v
            Organization
                |
                v
            AI Capability
                |
                v
            entitled=True

        If enabled=True is requested, entitlement must be granted
        at the same time.

        If enabled=False, the capability remains entitled but disabled.
        """

        org_parameter = await self._get_org_parameter(
            org_id=org_id,
            param_id=param_id,
        )

        if not org_parameter:

            raise ValueError(
                "AI capability does not exist for this organization"
            )

        # ----------------------------------------------------
        # Assign entitlement
        # ----------------------------------------------------

        org_parameter.entitled = True

        # ----------------------------------------------------
        # Optional immediate activation
        # ----------------------------------------------------

        if enabled:
            org_parameter.enabled = True

        org_parameter.updated_at = (
            datetime.now(timezone.utc)
        )

        audit = AuditLog(
            organization_id=org_id,
            action="ASSIGN_AI_PARAMETER_ENTITLEMENT",
            resource_type="organization_ai_parameter",
            resource_id=str(
                org_parameter.parameter_id
            ),
            details={
                "entitled": True,
                "enabled": bool(
                    org_parameter.enabled
                ),
            },
        )

        self.db.add(audit)

        await self.db.commit()

        await self.db.refresh(org_parameter)

        return {
            "success": True,
            "organization_id": str(org_id),
            "parameter_id": str(
                org_parameter.parameter_id
            ),
            "entitled": bool(
                org_parameter.entitled
            ),
            "enabled": bool(
                org_parameter.enabled
            ),
        }

    # ========================================================
    # REVOKE ENTITLEMENT
    # ========================================================

    async def revoke_entitlement(
        self,
        org_id: uuid.UUID,
        param_id: uuid.UUID,
    ) -> Dict[str, Any]:
        """
        Revoke an AI capability from one organization.

        Revocation automatically disables the capability.

        Result:

            entitled=False
            enabled=False
        """

        org_parameter = await self._get_org_parameter(
            org_id=org_id,
            param_id=param_id,
        )

        if not org_parameter:

            raise ValueError(
                "AI capability entitlement does not exist "
                "for this organization"
            )

        org_parameter.entitled = False
        org_parameter.enabled = False
        org_parameter.updated_at = (
            datetime.now(timezone.utc)
        )

        audit = AuditLog(
            organization_id=org_id,
            action="REVOKE_AI_PARAMETER_ENTITLEMENT",
            resource_type="organization_ai_parameter",
            resource_id=str(
                org_parameter.parameter_id
            ),
            details={
                "entitled": False,
                "enabled": False,
            },
        )

        self.db.add(audit)

        await self.db.commit()

        await self.db.refresh(org_parameter)

        return {
            "success": True,
            "organization_id": str(org_id),
            "parameter_id": str(
                org_parameter.parameter_id
            ),
            "entitled": False,
            "enabled": False,
        }

    # ========================================================
    # UPDATE CONFIGURATION
    # ========================================================

    async def update_parameter_config(
        self,
        org_id: uuid.UUID,
        param_id: uuid.UUID,
        config_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Update configuration for one organization's AI capability.

        Configuration changes are always organization scoped.
        """

        org_parameter = await self._get_org_parameter(
            org_id=org_id,
            param_id=param_id,
        )

        if not org_parameter:

            raise ValueError(
                "Parameter entitlement not found for this organization"
            )

        # ----------------------------------------------------
        # ENABLED
        # ----------------------------------------------------

        if "enabled" in config_data:

            requested_enabled = bool(
                config_data["enabled"]
            )

            if (
                requested_enabled
                and not org_parameter.entitled
            ):
                raise ValueError(
                    "Cannot enable an AI capability "
                    "without entitlement"
                )

            org_parameter.enabled = requested_enabled

        # ----------------------------------------------------
        # CONFIDENCE
        # ----------------------------------------------------

        if "confidence_threshold" in config_data:

            confidence = float(
                config_data[
                    "confidence_threshold"
                ]
            )

            if not 0.0 <= confidence <= 1.0:

                raise ValueError(
                    "confidence_threshold must be "
                    "between 0.0 and 1.0"
                )

            org_parameter.confidence_threshold = confidence

        # ----------------------------------------------------
        # FPS
        # ----------------------------------------------------

        if "sampling_fps" in config_data:

            fps = float(
                config_data["sampling_fps"]
            )

            if not 1.0 <= fps <= 60.0:

                raise ValueError(
                    "sampling_fps must be "
                    "between 1 and 60"
                )

            org_parameter.sampling_fps = fps

        # ----------------------------------------------------
        # PROCESSING MODE
        # ----------------------------------------------------

        if "processing_mode" in config_data:

            processing_mode = str(
                config_data["processing_mode"]
            ).strip()

            allowed_modes = {
                "Real-time",
                "Realtime",
                "Batch",
            }

            if processing_mode not in allowed_modes:

                raise ValueError(
                    "Invalid processing_mode. "
                    "Allowed values: Real-time, Batch"
                )

            org_parameter.processing_mode = (
                processing_mode
            )

        # ----------------------------------------------------
        # DEVICE
        # ----------------------------------------------------

        if "device_preference" in config_data:

            device = str(
                config_data["device_preference"]
            ).upper()

            if device not in {
                "CPU",
                "GPU",
            }:

                raise ValueError(
                    "device_preference must be CPU or GPU"
                )

            org_parameter.device_preference = device

        # ----------------------------------------------------
        # ALERT
        # ----------------------------------------------------

        if "alert_enabled" in config_data:

            org_parameter.alert_enabled = bool(
                config_data["alert_enabled"]
            )

        # ----------------------------------------------------
        # RETENTION
        # ----------------------------------------------------

        if "retention_days" in config_data:

            retention_days = int(
                config_data["retention_days"]
            )

            if retention_days < 1:

                raise ValueError(
                    "retention_days must be greater than 0"
                )

            org_parameter.retention_days = (
                retention_days
            )

        # ----------------------------------------------------
        # JSON CONFIGURATION
        # ----------------------------------------------------

        if "configuration_json" in config_data:

            configuration = (
                config_data["configuration_json"]
            )

            if not isinstance(
                configuration,
                dict,
            ):

                raise ValueError(
                    "configuration_json must be an object"
                )

            org_parameter.configuration_json = (
                configuration
            )

        # ----------------------------------------------------
        # CAMERA ASSIGNMENTS
        # ----------------------------------------------------

        if "camera_ids" in config_data:

            camera_ids = (
                config_data["camera_ids"]
                or []
            )

            if not isinstance(
                camera_ids,
                list,
            ):

                raise ValueError(
                    "camera_ids must be a list"
                )

            # Validate camera ownership
            if camera_ids:
                from app.models.camera import Camera
                from app.models.tenant import Tenant

                parsed_cam_uuids = []
                for cid in camera_ids:
                    try:
                        parsed_cam_uuids.append(uuid.UUID(str(cid)))
                    except ValueError:
                        raise ValueError(f"Invalid camera UUID: {cid}")

                valid_cams_query = (
                    select(Camera.id)
                    .join(Tenant, Camera.tenant_id == Tenant.id)
                    .where(
                        Camera.id.in_(parsed_cam_uuids),
                        Tenant.organization_id == org_id,
                    )
                )
                valid_cams_res = await self.db.execute(valid_cams_query)
                valid_cam_ids = set(valid_cams_res.scalars().all())

                for c_uuid in parsed_cam_uuids:
                    if c_uuid not in valid_cam_ids:
                        raise ValueError(
                            f"Camera {c_uuid} does not belong to organization {org_id}"
                        )

            # Remove existing assignments.
            await self.db.execute(
                delete(
                    ParameterCameraAssignment
                ).where(
                    ParameterCameraAssignment.organization_id
                    == org_id,
                    ParameterCameraAssignment.parameter_id
                    == org_parameter.parameter_id,
                )
            )

            # Create new assignments.
            for camera_id in camera_ids:

                camera_uuid = uuid.UUID(str(camera_id))

                assignment = (
                    ParameterCameraAssignment(
                        organization_id=org_id,
                        camera_id=camera_uuid,
                        parameter_id=(
                            org_parameter.parameter_id
                        ),
                        enabled=True,
                    )
                )

                self.db.add(assignment)

        # ----------------------------------------------------
        # Mark configured
        # ----------------------------------------------------

        org_parameter.configured = True

        org_parameter.updated_at = (
            datetime.now(timezone.utc)
        )

        # ----------------------------------------------------
        # Audit
        # ----------------------------------------------------

        audit = AuditLog(
            organization_id=org_id,
            action="UPDATE_AI_PARAMETER_CONFIG",
            resource_type="organization_ai_parameter",
            resource_id=str(
                org_parameter.parameter_id
            ),
            details=config_data,
        )

        self.db.add(audit)

        await self.db.commit()

        await self.db.refresh(org_parameter)

        return {
            "success": True,
            "organization_id": str(org_id),
            "parameter_id": str(
                org_parameter.parameter_id
            ),
            "enabled": bool(
                org_parameter.enabled
            ),
            "entitled": bool(
                org_parameter.entitled
            ),
            "configured": bool(
                org_parameter.configured
            ),
        }

    # ========================================================
    # GET CATALOG
    # ========================================================

    async def get_catalog_items(
        self,
    ) -> List[AIParameterCatalog]:
        """
        Return global master catalog.

        This is NOT organization-specific.
        """

        result = await self.db.execute(
            select(AIParameterCatalog)
            .where(
                AIParameterCatalog.is_active == True
            )
            .order_by(
                AIParameterCatalog.service_number
            )
        )

        return list(
            result.scalars().all()
        )