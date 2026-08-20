--
-- PostgreSQL database dump
--

\restrict vtMpnA82iU7pAQFOeJbklCk7B80Z3q8rYc0iFDnydV2uCTbfiSeoDVpFX1aXqL6

-- Dumped from database version 18.4 (Ubuntu 18.4-0ubuntu0.26.04.1)
-- Dumped by pg_dump version 18.4 (Ubuntu 18.4-0ubuntu0.26.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: sentriqvision
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO sentriqvision;

--
-- Name: vector; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA public;


--
-- Name: EXTENSION vector; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION vector IS 'vector data type and ivfflat and hnsw access methods';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: ai_inference_logs; Type: TABLE; Schema: public; Owner: kirti
--

CREATE TABLE public.ai_inference_logs (
    id uuid NOT NULL,
    organization_id uuid NOT NULL,
    camera_id uuid,
    parameter_code character varying(100) NOT NULL,
    model_name character varying(100) NOT NULL,
    device character varying(50) NOT NULL,
    latency_ms double precision NOT NULL,
    fps double precision NOT NULL,
    result_count integer NOT NULL,
    status character varying(50) NOT NULL,
    error_message text,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.ai_inference_logs OWNER TO kirti;

--
-- Name: ai_parameter_catalog; Type: TABLE; Schema: public; Owner: kirti
--

CREATE TABLE public.ai_parameter_catalog (
    id uuid NOT NULL,
    service_number integer NOT NULL,
    code character varying(100) NOT NULL,
    name character varying(255) NOT NULL,
    domain character varying(100) NOT NULL,
    description text NOT NULL,
    hardware_requirement character varying(50) NOT NULL,
    processing_mode character varying(50) NOT NULL,
    default_confidence double precision NOT NULL,
    default_fps double precision NOT NULL,
    configuration_schema json,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.ai_parameter_catalog OWNER TO kirti;

--
-- Name: alert_rules; Type: TABLE; Schema: public; Owner: kirti
--

CREATE TABLE public.alert_rules (
    id uuid NOT NULL,
    tenant_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    event_type character varying(100) NOT NULL,
    condition_json json NOT NULL,
    actions_json json NOT NULL,
    severity character varying(50) NOT NULL,
    is_enabled boolean NOT NULL,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.alert_rules OWNER TO kirti;

--
-- Name: alerts; Type: TABLE; Schema: public; Owner: kirti
--

CREATE TABLE public.alerts (
    id uuid NOT NULL,
    tenant_id uuid NOT NULL,
    rule_id uuid,
    event_id uuid,
    severity character varying(50) NOT NULL,
    title character varying(255) NOT NULL,
    description text,
    status character varying(50) NOT NULL,
    acknowledged_by uuid,
    acknowledged_at timestamp with time zone,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.alerts OWNER TO kirti;

--
-- Name: audit_logs; Type: TABLE; Schema: public; Owner: kirti
--

CREATE TABLE public.audit_logs (
    id uuid NOT NULL,
    organization_id uuid,
    user_id uuid,
    action character varying(100) NOT NULL,
    resource_type character varying(100) NOT NULL,
    resource_id character varying(255),
    details json,
    ip_address character varying(50),
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.audit_logs OWNER TO kirti;

--
-- Name: camera_health; Type: TABLE; Schema: public; Owner: kirti
--

CREATE TABLE public.camera_health (
    id uuid NOT NULL,
    camera_id uuid NOT NULL,
    is_online boolean NOT NULL,
    latency_ms double precision,
    fps_actual double precision,
    packet_loss double precision,
    checked_at timestamp with time zone NOT NULL
);


ALTER TABLE public.camera_health OWNER TO kirti;

--
-- Name: cameras; Type: TABLE; Schema: public; Owner: kirti
--

CREATE TABLE public.cameras (
    id uuid NOT NULL,
    tenant_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    location character varying(255),
    rtsp_url character varying(500) NOT NULL,
    substream_url character varying(500),
    fps_sampling integer NOT NULL,
    status character varying(50) NOT NULL,
    roi_polygons json,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.cameras OWNER TO kirti;

--
-- Name: event_frames; Type: TABLE; Schema: public; Owner: kirti
--

CREATE TABLE public.event_frames (
    id uuid NOT NULL,
    event_id uuid NOT NULL,
    frame_type character varying(50) NOT NULL,
    storage_path character varying(500) NOT NULL,
    width integer,
    height integer
);


ALTER TABLE public.event_frames OWNER TO kirti;

--
-- Name: events; Type: TABLE; Schema: public; Owner: kirti
--

CREATE TABLE public.events (
    id uuid NOT NULL,
    tenant_id uuid NOT NULL,
    camera_id uuid,
    event_type character varying(100) NOT NULL,
    severity character varying(50) NOT NULL,
    confidence double precision NOT NULL,
    payload json NOT NULL,
    "timestamp" timestamp with time zone NOT NULL
);


ALTER TABLE public.events OWNER TO kirti;

--
-- Name: face_embeddings; Type: TABLE; Schema: public; Owner: kirti
--

CREATE TABLE public.face_embeddings (
    id uuid NOT NULL,
    person_id uuid NOT NULL,
    embedding public.vector(512) NOT NULL,
    quality_score double precision NOT NULL,
    bounding_box json,
    source_image_path character varying(500),
    aligned_face_path character varying(500),
    model_version character varying(50) NOT NULL,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.face_embeddings OWNER TO kirti;

--
-- Name: organization_ai_parameters; Type: TABLE; Schema: public; Owner: kirti
--

CREATE TABLE public.organization_ai_parameters (
    id uuid NOT NULL,
    organization_id uuid NOT NULL,
    parameter_id uuid NOT NULL,
    enabled boolean NOT NULL,
    entitled boolean NOT NULL,
    configured boolean NOT NULL,
    confidence_threshold double precision NOT NULL,
    sampling_fps double precision NOT NULL,
    processing_mode character varying(50) NOT NULL,
    device_preference character varying(50) NOT NULL,
    alert_enabled boolean NOT NULL,
    retention_days integer NOT NULL,
    configuration_json json,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.organization_ai_parameters OWNER TO kirti;

--
-- Name: organizations; Type: TABLE; Schema: public; Owner: kirti
--

CREATE TABLE public.organizations (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.organizations OWNER TO kirti;

--
-- Name: parameter_camera_assignments; Type: TABLE; Schema: public; Owner: kirti
--

CREATE TABLE public.parameter_camera_assignments (
    id uuid NOT NULL,
    organization_id uuid NOT NULL,
    camera_id uuid NOT NULL,
    parameter_id uuid NOT NULL,
    enabled boolean NOT NULL,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.parameter_camera_assignments OWNER TO kirti;

--
-- Name: permissions; Type: TABLE; Schema: public; Owner: kirti
--

CREATE TABLE public.permissions (
    id uuid NOT NULL,
    code character varying(100) NOT NULL,
    module character varying(100) NOT NULL,
    description text
);


ALTER TABLE public.permissions OWNER TO kirti;

--
-- Name: persons; Type: TABLE; Schema: public; Owner: kirti
--

CREATE TABLE public.persons (
    id uuid NOT NULL,
    tenant_id uuid NOT NULL,
    external_id character varying(100),
    full_name character varying(255) NOT NULL,
    department character varying(100),
    access_level character varying(50) NOT NULL,
    is_blacklisted boolean NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.persons OWNER TO kirti;

--
-- Name: recordings; Type: TABLE; Schema: public; Owner: kirti
--

CREATE TABLE public.recordings (
    id uuid NOT NULL,
    camera_id uuid NOT NULL,
    file_path character varying(500) NOT NULL,
    file_size_bytes bigint NOT NULL,
    duration_seconds double precision NOT NULL,
    start_time timestamp with time zone NOT NULL,
    end_time timestamp with time zone NOT NULL
);


ALTER TABLE public.recordings OWNER TO kirti;

--
-- Name: role_permissions; Type: TABLE; Schema: public; Owner: kirti
--

CREATE TABLE public.role_permissions (
    role_id uuid NOT NULL,
    permission_id uuid NOT NULL
);


ALTER TABLE public.role_permissions OWNER TO kirti;

--
-- Name: roles; Type: TABLE; Schema: public; Owner: kirti
--

CREATE TABLE public.roles (
    id uuid NOT NULL,
    tenant_id uuid,
    name character varying(100) NOT NULL,
    description text,
    is_system boolean NOT NULL
);


ALTER TABLE public.roles OWNER TO kirti;

--
-- Name: tenants; Type: TABLE; Schema: public; Owner: kirti
--

CREATE TABLE public.tenants (
    id uuid NOT NULL,
    organization_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    code character varying(100) NOT NULL,
    config json NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.tenants OWNER TO kirti;

--
-- Name: user_roles; Type: TABLE; Schema: public; Owner: kirti
--

CREATE TABLE public.user_roles (
    user_id uuid NOT NULL,
    role_id uuid NOT NULL
);


ALTER TABLE public.user_roles OWNER TO kirti;

--
-- Name: users; Type: TABLE; Schema: public; Owner: kirti
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    tenant_id uuid NOT NULL,
    email character varying(255) NOT NULL,
    password_hash character varying(255) NOT NULL,
    full_name character varying(255) NOT NULL,
    is_superuser boolean NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.users OWNER TO kirti;

--
-- Data for Name: ai_inference_logs; Type: TABLE DATA; Schema: public; Owner: kirti
--

COPY public.ai_inference_logs (id, organization_id, camera_id, parameter_code, model_name, device, latency_ms, fps, result_count, status, error_message, created_at) FROM stdin;
\.


--
-- Data for Name: ai_parameter_catalog; Type: TABLE DATA; Schema: public; Owner: kirti
--

COPY public.ai_parameter_catalog (id, service_number, code, name, domain, description, hardware_requirement, processing_mode, default_confidence, default_fps, configuration_schema, is_active, created_at) FROM stdin;
ba091ec7-9a0e-42de-a349-0954db03e072	1	FACE_DETECTION	Face Detection	Face & Identity	Detects face bounding boxes and facial landmark points.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750651+05:30
7300be74-ce98-477e-bcdd-f945699e8039	2	FACE_RECOGNITION	Face Recognition	Face & Identity	512d vector embedding matching using ArcFace and pgvector.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750658+05:30
6ddef5a8-df19-4b35-8b41-2d3a46d73af9	3	FACE_LIVENESS	Face Liveness	Face & Identity	Anti-spoofing liveness detection against 2D photos and screens.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750661+05:30
0754c127-34f5-48ea-8e9a-0d4de67ba813	4	FACE_QUALITY_ANALYSIS	Face Quality Analysis	Face & Identity	Evaluates sharpness, head pose pitch/yaw, and illumination quality.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750664+05:30
305f9726-81b8-49f5-b7be-d1f80053ff3b	5	FACE_TRACKING	Face Tracking	Face & Identity	Assigns persistent IDs to facial tracks across video frames.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750667+05:30
29c21f33-418d-463f-9c21-673daf5c933c	6	PERSON_DETECTION	Person Detection	People & Behavior	Detects human bodies in indoor and outdoor surveillance feeds.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750669+05:30
5cad4a15-9a33-4d23-bf15-44bdb2935137	7	PERSON_TRACKING	Person Tracking	People & Behavior	Tracks person trajectories and spatial movement over time.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750672+05:30
ebd081c5-b2ef-489c-aa2b-a833762733ba	8	CROWD_DETECTION	Crowd Detection	People & Behavior	Measures crowd density and detects dangerous crowding levels.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750674+05:30
2f4c3200-b45f-4482-b2f1-7cc9e71033f0	9	LOITERING_DETECTION	Loitering Detection	People & Behavior	Flags individuals staying in designated zones past threshold duration.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750677+05:30
df60e01d-a5dd-4e71-b666-957bc465b8cb	10	INTRUSION_DETECTION	Intrusion Detection	Security & Access	Triggers alerts when humans/vehicles breach defined security polygons.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750679+05:30
4386b6aa-672c-4c8a-b8ab-75b12bbe1236	11	RESTRICTED_ZONE_DETECTION	Restricted Zone Detection	Security & Access	Monitors secure perimeters and confidential areas for unauthorized entry.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750682+05:30
08e7a6b3-71ff-4607-a7bd-dd663ae76bc0	12	LINE_CROSSING_DETECTION	Line Crossing Detection	Security & Access	Detects directional crossing across virtual tripwire lines.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750684+05:30
117216d0-d735-4552-92e5-ef498dd89274	13	DWELL_TIME_DETECTION	Dwell Time Detection	Analytics & Insights	Calculates total time subjects remain within specific retail/security areas.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750687+05:30
c08c17d7-9437-4935-b6d1-f3ef453b4271	14	FALL_DETECTION	Fall Detection	Safety & Health	Detects sudden human falls and unresponsiveness for emergency dispatch.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750689+05:30
b45f435c-2c5f-4db1-bfdc-18d99e1c61f2	15	FIGHT_DETECTION	Fight Detection	Security & Access	Monitors physical altercations, rapid violent gestures, and brawls.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750691+05:30
50a5640b-0177-4e2c-abd2-48380d37a5f3	16	VIOLENCE_DETECTION	Violence Detection	Security & Access	AI model detecting physical aggression and violent interactions.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750695+05:30
0d363f6a-68be-4f7b-811e-c49947613d28	17	ABANDONED_OBJECT_DETECTION	Abandoned Object Detection	Security & Access	Flags stationary unattended baggage, packages, or suspicious items.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.7507+05:30
3687ff57-9933-4113-9776-b314dc96a36f	18	LEFT_OBJECT_DETECTION	Left Object Detection	Security & Access	Detects objects placed and left behind in public transit/spaces.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750703+05:30
ccc5fd17-3f4c-47d1-86b5-ea2d5e2dd6df	19	WRONG_DIRECTION_DETECTION	Wrong Direction Detection	Transportation	Detects vehicles or pedestrians moving counter to designated flow.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750706+05:30
79978747-b2bd-4a7f-a198-0a5407d835f7	20	PPE_HELMET_DETECTION	PPE Helmet Detection	Safety & Health	Verifies hardhat compliance on construction and industrial sites.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750708+05:30
4ef4f388-0729-4097-9ff6-a1e0a0aece56	21	PPE_SAFETY_VEST_DETECTION	PPE Safety Vest Detection	Safety & Health	Verifies high-visibility safety vest compliance.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750711+05:30
6c12994d-1a18-477b-a8a4-876c9d638654	22	PPE_MASK_DETECTION	PPE Mask Detection	Safety & Health	Detects facial mask and respirator compliance.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750713+05:30
3ec3a864-19d8-4d55-b49e-8f75247eb549	23	SMOKE_DETECTION	Smoke Detection	Safety & Health	Early optical detection of rising smoke plumes.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750716+05:30
0f3dde44-f08a-4066-bfbd-b6872e0d67c9	24	FIRE_DETECTION	Fire Detection	Safety & Health	Optical and thermal flame detection for fire hazard alerting.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750719+05:30
68ea5a2e-4581-42f2-8e95-b1fb6a528ae7	25	GLASS_BREAK_DETECTION	Glass Break Detection	Security & Access	Visual and acoustic glass shatter and forced entry detection.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750721+05:30
ef7b1fba-8f81-4f8d-bd7a-81c26e1184ce	26	VEHICLE_DETECTION	Vehicle Detection	Transportation	Detects automobiles, trucks, buses, motorcycles, and bicycles.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750724+05:30
218274c6-e131-4153-83a3-18f49d1f009d	27	VEHICLE_TRACKING	Vehicle Tracking	Transportation	Multi-camera vehicle trajectory tracking and speed estimation.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750726+05:30
4d17caeb-67fa-40c3-8f87-99d0d9b672fa	28	ANPR_LPR	ANPR / LPR	Transportation	Automatic Number Plate Recognition with region format matching.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750728+05:30
176ec945-4da5-400d-9a8b-4ddf2e2b5b4b	29	LICENSE_PLATE_OCR	License Plate OCR	Transportation	High-accuracy optical character recognition for license plates.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.75073+05:30
687f5223-3b75-4fa9-89e9-ab2aecd8acf8	30	VEHICLE_COLOR_CLASSIFICATION	Vehicle Color Classification	Transportation	Classifies primary and secondary vehicle paint colors.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750733+05:30
b321edbd-3b91-4d19-ac86-d5f78fff83a7	31	VEHICLE_TYPE_CLASSIFICATION	Vehicle Type Classification	Transportation	Classifies vehicle body types (Sedan, SUV, Pickup, Van, Truck).	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750735+05:30
4fdb5bb7-383b-4e1e-8e04-e8397db1a0d5	32	VEHICLE_MAKE_MODEL_CLASSIFICATION	Vehicle Make/Model Classification	Transportation	Identifies vehicle manufacturer make and model series.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750737+05:30
2bcc4420-6cfa-4477-9700-118f1ce4b3a1	33	SEATBELT_DETECTION	Seatbelt Detection	Safety & Health	Detects driver and passenger seatbelt compliance inside vehicles.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750739+05:30
830d8388-0cb5-4d32-aa5e-a3f4858b73c0	34	WRONG_PARKING_DETECTION	Wrong Parking Detection	Transportation	Detects illegal parking, blocked emergency lanes, and double parking.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750741+05:30
f62fe28e-3cf4-414d-a85a-cb53d42632f9	35	PARKING_OCCUPANCY	Parking Occupancy	Transportation	Monitors open vs occupied parking stall availability in real time.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750744+05:30
f743a660-162d-450e-bafc-a9bb900b93d2	36	VEHICLE_SPEED_ESTIMATION	Vehicle Speed Estimation	Transportation	Calculates vehicle velocity across calibrated camera zones.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750746+05:30
27751110-600e-4c3a-a280-58715c9ecb57	37	TRAFFIC_FLOW_ANALYSIS	Traffic Flow Analysis	Transportation	Analyzes traffic volume throughput, congestion, and average speed.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750748+05:30
86df68a7-8d5a-4638-a21b-37ee1389b5f7	38	OBJECT_COUNTING	Object Counting	Analytics & Insights	Counts target objects crossing virtual lines or inside ROI zones.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.75075+05:30
7cad19da-93d1-4932-87a1-2908b1f35d92	39	PEOPLE_COUNTING	People Counting	Analytics & Insights	Real-time footfall counting for entry/exit capacity management.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750753+05:30
0ac5e123-1f2f-4cfc-b036-353a0b859c6c	40	QUEUE_DETECTION	Queue Detection	Analytics & Insights	Detects queue formation at checkout counters and service desks.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750755+05:30
a051f70f-7c0a-48fe-824a-4d7b7d4691b3	41	QUEUE_LENGTH_ANALYSIS	Queue Length Analysis	Analytics & Insights	Measures active queue depth, waiting times, and service bottlenecks.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750757+05:30
fe680993-c2bd-4d0c-b081-a6af1a047f31	42	OCCUPANCY_ANALYSIS	Occupancy Analysis	Analytics & Insights	Tracks real-time facility occupancy against maximum safety limits.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750759+05:30
1dc570b2-aa15-47fe-9a47-d93585ca8f7a	43	HEATMAP_ANALYTICS	Heatmap Analytics	Analytics & Insights	Generates spatial movement and foot traffic intensity heatmaps.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750762+05:30
303d2ead-f447-47b9-be02-68c18a9ee517	44	OCR	General OCR Engine	Analytics & Insights	Extracts printed text from shipping containers, badges, and labels.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750764+05:30
df77f086-b3b2-45b0-a013-c8153f748d03	45	DOCUMENT_DETECTION	Document Detection	Security & Access	Detects physical ID cards, passports, and driver licenses.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750766+05:30
71d8eb7d-62d2-4e31-85d4-0f0e7cb11290	46	CAMERA_TAMPER_DETECTION	Camera Tamper Detection	Device & System	Detects camera spray paint, defocus, tilt, or obstruction.	CPU/GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750768+05:30
cc8bac03-c480-4d02-a052-357889a6ad1d	47	CAMERA_OFFLINE_DETECTION	Camera Offline Detection	Device & System	Monitors stream loss, RTSP timeouts, and network disconnects.	CPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750771+05:30
b5e273f7-c4b7-4dbd-9de4-66f821a4fafe	48	ANOMALY_DETECTION	General Anomaly Detection	Intelligence	Unsupervised AI flagging abnormal visual patterns and behaviors.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750773+05:30
abca03e3-5130-4400-b711-78aac0d16b51	49	BEHAVIOR_ANOMALY_DETECTION	Behavior Anomaly Detection	Intelligence	Flags errant human movements, panic running, or erratic behavior.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750776+05:30
99d73b40-034a-4813-bdeb-48a6b90550c8	50	SLIP_TRIP_DETECTION	Slip & Trip Detection	Safety & Health	Detects hazardous slips, trips, and industrial surface falls.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750778+05:30
e0a8705e-7c3b-4076-988e-e8d3f3bc78b4	51	ACCESS_CONTROL	Access Control System	Security & Access	Integrates face/ANPR biometrics with physical door relays and gates.	CPU/GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.75078+05:30
ef177366-dee5-4be4-b9dc-0693181cc91b	52	EVENT_CORRELATION	Event Correlation Engine	Intelligence	Correlates multi-camera events into unified incident stories.	CPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750782+05:30
5a761f99-4405-4d3f-9bf0-b25e1a68322a	53	AI_RULE_ENGINE	AI Rule Engine	Intelligence	Evaluates multi-condition spatial-temporal logic rules for alert dispatch.	CPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750785+05:30
1ebcb63c-5fc5-4838-99fa-963e909d8512	54	ALERT_INTELLIGENCE	Alert Intelligence & RAG	Intelligence	LLM-assisted alert summaries, root cause, and dispatch actions.	GPU	Real-time	0.7	10	{"confidence_slider": true, "sampling_fps": true, "device_select": true, "camera_assignment": true, "alert_policy": true}	t	2026-08-18 11:23:08.750787+05:30
\.


--
-- Data for Name: alert_rules; Type: TABLE DATA; Schema: public; Owner: kirti
--

COPY public.alert_rules (id, tenant_id, name, event_type, condition_json, actions_json, severity, is_enabled, created_at) FROM stdin;
\.


--
-- Data for Name: alerts; Type: TABLE DATA; Schema: public; Owner: kirti
--

COPY public.alerts (id, tenant_id, rule_id, event_id, severity, title, description, status, acknowledged_by, acknowledged_at, created_at) FROM stdin;
8255e539-3b6c-43e3-bab6-90c11b4ea34b	e5940184-3c6c-4ae0-907b-e4f040336e7b	\N	\N	CRITICAL	Unauthorized Night Perimeter Intrusion	Unknown target detected near Perimeter Gate A zone after 22:00 UTC	NEW	\N	\N	2026-08-18 12:13:49.669561+05:30
62dab139-8e88-422b-8f34-6ff4f1a1360e	e5940184-3c6c-4ae0-907b-e4f040336e7b	\N	\N	CRITICAL	Blacklisted Subject at Server Vault	pgvector 98.6% similarity match to blacklisted individual #PER-9912	ACKNOWLEDGED	\N	\N	2026-08-18 12:13:49.669634+05:30
59a94c78-aa54-4b77-a176-619012645bf2	e5940184-3c6c-4ae0-907b-e4f040336e7b	\N	\N	MEDIUM	PPE Safety Hardhat & Vest Violation	Worker operating forklift without required safety helmet and vest	RESOLVED	\N	\N	2026-08-18 12:13:49.669661+05:30
\.


--
-- Data for Name: audit_logs; Type: TABLE DATA; Schema: public; Owner: kirti
--

COPY public.audit_logs (id, organization_id, user_id, action, resource_type, resource_id, details, ip_address, created_at) FROM stdin;
1a9056bd-c4f2-4307-9be5-3b912cf2fed6	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	3f0e93db-2dba-4ee8-bd70-86903ef893f6	CREATE_ORGANIZATION	organization	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	{"name": "foundit", "slug": "foundit"}	\N	2026-08-18 12:30:08.999921+05:30
65926e30-4661-4afb-8a70-805d8d6ccae0	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	\N	TOGGLE_AI_PARAMETER	organization_ai_parameter	ba091ec7-9a0e-42de-a349-0954db03e072	{"enabled": false, "entitled": true}	\N	2026-08-18 15:53:40.896341+05:30
9511f8f6-121e-4a8e-a835-dc9b63595357	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	\N	TOGGLE_AI_PARAMETER	organization_ai_parameter	303d2ead-f447-47b9-be02-68c18a9ee517	{"enabled": true, "entitled": true}	\N	2026-08-18 16:02:18.189823+05:30
7a9ad37e-39ad-49ba-95d8-cbb3759aea27	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	\N	TOGGLE_AI_PARAMETER	organization_ai_parameter	ba091ec7-9a0e-42de-a349-0954db03e072	{"enabled": true, "entitled": true}	\N	2026-08-18 16:06:39.536598+05:30
7bdd25d9-5832-47c6-83d4-5e5bae8c4fbb	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	\N	TOGGLE_AI_PARAMETER	organization_ai_parameter	ba091ec7-9a0e-42de-a349-0954db03e072	{"enabled": false, "entitled": true}	\N	2026-08-18 16:06:45.27956+05:30
26ecf228-9fe2-4aaf-9c65-dd2a6609b34c	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	\N	TOGGLE_AI_PARAMETER	organization_ai_parameter	7300be74-ce98-477e-bcdd-f945699e8039	{"enabled": false, "entitled": true}	\N	2026-08-18 16:53:00.171732+05:30
6b6d0b28-bcec-46b8-8b1e-573e71a64073	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	\N	TOGGLE_AI_PARAMETER	organization_ai_parameter	7300be74-ce98-477e-bcdd-f945699e8039	{"enabled": true, "entitled": true}	\N	2026-08-18 16:53:01.84295+05:30
fb30d3c3-aaef-4996-8612-c25a996ff49f	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	\N	TOGGLE_AI_PARAMETER	organization_ai_parameter	ba091ec7-9a0e-42de-a349-0954db03e072	{"enabled": true, "entitled": true}	\N	2026-08-18 17:02:19.174554+05:30
355d7c8f-6dcb-4d49-a2f0-a0e1d0e47661	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	\N	TOGGLE_AI_PARAMETER	organization_ai_parameter	ba091ec7-9a0e-42de-a349-0954db03e072	{"enabled": false, "entitled": true}	\N	2026-08-18 17:02:20.572866+05:30
1bc4b901-6cb1-40ed-b9f6-8213dc50b48b	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	\N	TOGGLE_AI_PARAMETER	organization_ai_parameter	cc8bac03-c480-4d02-a052-357889a6ad1d	{"enabled": true, "entitled": true}	\N	2026-08-18 17:02:32.459258+05:30
10d636aa-54c7-4a8d-b096-1ffd3f2ea8d2	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	\N	TOGGLE_AI_PARAMETER	organization_ai_parameter	ba091ec7-9a0e-42de-a349-0954db03e072	{"enabled": true, "entitled": true}	\N	2026-08-18 23:05:11.913575+05:30
7dfc5d03-f92e-40bb-a0ac-ee0a49989bf6	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	\N	TOGGLE_AI_PARAMETER	organization_ai_parameter	ba091ec7-9a0e-42de-a349-0954db03e072	{"enabled": false, "entitled": true}	\N	2026-08-18 23:05:13.430218+05:30
\.


--
-- Data for Name: camera_health; Type: TABLE DATA; Schema: public; Owner: kirti
--

COPY public.camera_health (id, camera_id, is_online, latency_ms, fps_actual, packet_loss, checked_at) FROM stdin;
\.


--
-- Data for Name: cameras; Type: TABLE DATA; Schema: public; Owner: kirti
--

COPY public.cameras (id, tenant_id, name, location, rtsp_url, substream_url, fps_sampling, status, roi_polygons, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: event_frames; Type: TABLE DATA; Schema: public; Owner: kirti
--

COPY public.event_frames (id, event_id, frame_type, storage_path, width, height) FROM stdin;
\.


--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: kirti
--

COPY public.events (id, tenant_id, camera_id, event_type, severity, confidence, payload, "timestamp") FROM stdin;
5ef25f7b-8ed7-4432-8745-9b0870c2c69f	e5940184-3c6c-4ae0-907b-e4f040336e7b	\N	FACE_RECOGNIZED	INFO	0.985	{"person_name": "John Doe", "role": "Executive", "match_score": 0.985}	2026-08-18 12:13:47.055375+05:30
542b2e6f-da6d-4411-971c-f04c64a99dbd	e5940184-3c6c-4ae0-907b-e4f040336e7b	\N	INTRUSION_DETECTED	CRITICAL	0.962	{"zone": "Server Vault ROI-1", "dwell_sec": 30}	2026-08-18 12:13:47.055417+05:30
1afe5939-9a3b-43c7-909d-a571018af5b6	e5940184-3c6c-4ae0-907b-e4f040336e7b	\N	PPE_VIOLATION	MEDIUM	0.91	{"missing_gear": ["helmet", "vest"]}	2026-08-18 12:13:47.055433+05:30
5b3de5d3-6b4f-430e-9192-80d505c813bb	e5940184-3c6c-4ae0-907b-e4f040336e7b	\N	ANPR_DETECTED	INFO	0.97	{"plate_number": "MH-02-CB-1234", "vehicle_type": "SEDAN", "color": "WHITE", "is_authorized": true}	2026-08-18 12:14:35.706386+05:30
\.


--
-- Data for Name: face_embeddings; Type: TABLE DATA; Schema: public; Owner: kirti
--

COPY public.face_embeddings (id, person_id, embedding, quality_score, bounding_box, source_image_path, aligned_face_path, model_version, created_at) FROM stdin;
2a1f67f0-b579-4037-aec3-4dd530569527	bd46806d-d06d-4280-9018-4a351b12dbd2	[0.0093434155,-0.015560228,-0.0022718944,0.065719485,0.0037662447,-0.030885495,0.016136099,0.035801973,-0.0007507322,0.028116183,0.07412392,-0.036455147,0.052508447,0.042939905,0.056878455,0.023809075,-0.0026673372,0.027436035,0.03747852,-0.073894076,-0.018809833,0.062244233,-0.018766725,-0.0005034214,-0.050102796,0.0678025,-0.07647332,-0.00093741727,-3.9948927e-06,-0.04135021,-0.033194713,0.057684336,0.055920035,0.0023727329,-0.037380464,-0.05588603,-0.049603056,0.014674301,-0.030566117,-0.05353231,-0.073161155,0.009539979,0.022054657,0.0377826,0.03836485,-0.026683006,0.027951859,0.047082815,-0.0300678,0.075275086,0.002185975,-0.0138559975,0.008342087,0.055659484,0.058352057,-0.023863835,-0.023436457,-0.04637197,0.033553768,-0.044349268,-0.024037775,0.076221876,0.07180548,-0.047434352,0.03547291,-0.054470506,-0.017363807,-0.02254465,0.023161568,0.051978223,0.02294911,0.01653521,0.07659268,0.07344453,-0.012035898,-0.035040356,0.00984089,0.007286615,-0.057590876,-0.046395134,-0.04577002,0.030013802,-0.011855428,0.032449253,0.00083462114,0.02051658,0.054380033,0.005523239,0.03898515,-0.044700358,0.071748435,-0.06063019,-0.072752304,0.00809357,-0.023400469,-0.051470287,-0.04316385,-0.06349498,-0.055015627,0.027486853,-0.06349006,-0.006327729,-0.06266996,0.06122065,0.058946054,0.04786049,-0.029847039,0.004415868,0.05826189,-0.015949024,-0.024380261,-0.060920827,0.067005344,0.05897289,-0.027214622,-0.04816496,-0.05961342,0.018030006,0.05307171,0.0018316491,0.044029534,-0.029577697,0.04525902,-0.016488375,-0.05314767,0.0067451205,0.03246337,0.014410326,-0.03115214,-0.026323596,-0.016270453,0.06245593,0.07157587,-0.07313632,-0.00042882943,0.041625146,0.041466583,-0.065031044,-0.0369262,-0.034635037,0.047082197,-0.043446947,-0.017033001,-0.0145913055,0.019788882,0.046708196,0.07336575,-0.002125871,-0.06467244,-0.05949165,0.05975276,0.03546877,-0.06983255,-0.074426845,-0.008688744,0.020248555,0.02277008,-0.015473961,0.008158507,-0.0037332093,0.030878643,-0.077314205,0.021536224,-0.065751836,-0.014657217,-0.06914911,-0.07727825,0.0018096641,0.009958431,0.008102545,0.059147447,0.062421374,0.033684883,-0.027563343,-0.06523809,-0.01853078,-0.066115625,0.048967123,-0.073255576,-0.0348239,-0.06765501,-0.05437591,-0.00476271,-0.0685045,-0.075730026,0.0045312755,0.0051084864,0.057151947,-0.069421425,0.011578864,-0.051468644,-0.074013345,0.07477711,0.06553436,0.0061192415,-0.005843933,0.03420716,-0.05302618,0.01174838,0.012861664,-0.023431761,-0.027367992,0.020546447,-0.01174606,0.035319794,-0.014040776,-0.06710637,0.01123982,-0.028459892,0.036997907,-0.039836332,0.03002769,0.04396162,-0.069528,0.06555239,0.02657698,-0.003888275,-0.040298767,0.014538894,0.037559427,0.058400523,0.014088299,-0.0035299184,-0.007846791,-0.06930431,-0.00071082165,-0.012484793,0.06732611,0.01181874,0.02082846,-0.031805772,0.0733357,-0.020628719,-0.031692825,0.05144463,0.039790615,-0.05950813,-0.06637565,-0.03798536,-0.042674422,0.07419663,0.077241816,-0.065123186,0.0429971,-0.0030352597,-0.026658138,0.075843364,0.0012565532,-0.0385197,0.07356485,0.07560984,-0.06874643,-0.022232056,-0.061154887,-0.06245885,-0.025043325,0.049416322,0.07229974,0.03326379,0.07693474,0.04765733,0.017715668,0.046512928,0.061831262,-0.0647736,-0.021806939,0.06782908,0.00859721,0.03672414,-0.0116806505,0.048003882,0.021652121,-0.0657715,0.034080576,0.0071307523,0.06726176,-0.01487703,0.036751494,0.05185279,-0.03418431,0.0007634434,-0.027953764,-0.05158912,0.018908639,0.068000734,0.029111104,0.04459828,-0.061087146,0.031757955,0.04940435,0.010183875,0.07025738,-0.03694012,-0.059916537,0.0682107,-0.071571015,-0.010328565,-0.029618528,0.022807244,-0.0074601397,-0.06386855,-0.05807115,-0.015577443,-0.014099976,0.06640709,-0.053825293,-0.032102082,-0.0064616753,0.07306382,0.0037354126,0.069732055,0.05541716,-0.010387944,0.03645957,-0.04654021,-0.016998002,0.05066283,-0.07372044,-0.03455709,-0.029889457,0.022732612,-0.04180232,0.047968257,-0.053728137,-0.0028794801,-0.04753308,-0.022580253,0.043059774,0.06397597,-0.007407564,0.004470383,-0.043565363,-0.07410613,-0.036845032,-0.030677564,0.021361377,0.035944812,-0.058836788,-0.05562223,-0.053480823,-0.009329397,-0.017520186,-0.015605461,0.00058381975,-0.016242877,-0.03354897,-0.0056046746,0.032219622,-0.074683756,-0.03812293,-0.03310641,0.04741699,-0.06536398,-0.02576029,-0.002521879,-0.016634377,-0.018165391,-0.06745118,0.06832269,0.03438436,-0.01988655,-0.009927437,-0.02124497,0.004237246,-0.04743683,-0.077432126,0.059547704,-0.026978346,0.008755006,0.01775217,0.05128569,0.067869306,0.012707028,0.07685009,0.043581393,0.042281993,0.0009997936,-0.018363945,0.040039547,-0.017344588,-0.005420349,0.0050550783,-0.0038687827,0.065391116,0.03190564,0.060250133,0.051899027,-0.025836475,-0.045835573,-0.069027185,-0.00017220547,0.066446364,-0.07310114,-0.041134756,0.04511636,0.044570595,-0.014907258,0.02801075,-0.023363648,0.05716089,0.07405707,-0.029641509,-0.008673651,-0.061254658,0.013087626,0.063130334,0.022261858,0.07625106,0.010038225,-0.036862656,0.055225387,0.022607708,0.055245068,0.00069174345,-0.0014389744,0.07597507,0.020519923,0.0122604165,0.037294626,-0.05446313,-0.02024601,-0.045532513,0.025915517,-0.0018235712,0.030477213,0.035832684,0.06959918,-0.07604292,-0.061165992,-0.022794714,0.04412539,-0.010293715,0.051115498,-0.027737876,0.031480808,-0.04060596,0.010307964,0.05762826,-0.014848295,-0.06010022,0.035879415,0.031753678,0.07206251,0.033130944,-0.035662178,0.017856956,0.077367865,0.04089339,0.036526747,0.0511165,0.0035420074,-0.04362465,0.02273521,0.062738374,-0.0009591783,-0.013551898,0.033499982,-0.048577663,0.00015082088,-0.033608165,-0.0037143484,-0.020176679,-0.043749686,-0.046129875,-0.04251582,-0.06967086,-0.012514575,-0.032484382,-0.032837443,-0.031223152,-0.06255973,0.042314846,-0.07617779,-0.021465128,0.026205579,-0.035864428,-0.0378824,-0.047581106,-0.05301936,-0.032569285,0.02002213,0.026426768,0.061683666,-0.011026797,-0.06472615,-0.0059289336,0.045962457,0.07248068,-0.07232102,-0.003054702,-0.0037227029,-0.027855754,0.042822402,0.04515112,0.07196027,0.032615885,0.072187796,0.02267504,0.05347178,0.06594583,0.052905023,-0.050960388,0.022116046,-0.017891135,-0.021825315,0.05302038,-0.0619777,-0.0250621,0.07424325,-0.0237444,-0.040351693,-0.05950256]	0.95	{"x": 100, "y": 80, "w": 200, "h": 200}	\N	\N	arcface_r100	2026-08-18 12:14:18.932996+05:30
\.


--
-- Data for Name: organization_ai_parameters; Type: TABLE DATA; Schema: public; Owner: kirti
--

COPY public.organization_ai_parameters (id, organization_id, parameter_id, enabled, entitled, configured, confidence_threshold, sampling_fps, processing_mode, device_preference, alert_enabled, retention_days, configuration_json, created_at, updated_at) FROM stdin;
6dd10649-ac32-4087-958b-8cab907fdefa	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	6ddef5a8-df19-4b35-8b41-2d3a46d73af9	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795043+05:30	2026-08-18 11:23:08.795046+05:30
3957d401-56de-484d-9da9-8e1a2809b56b	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	0754c127-34f5-48ea-8e9a-0d4de67ba813	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795064+05:30	2026-08-18 11:23:08.795067+05:30
de27f39d-2413-44ae-aac8-3949f4564c23	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	305f9726-81b8-49f5-b7be-d1f80053ff3b	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795086+05:30	2026-08-18 11:23:08.79509+05:30
78adfb5d-453e-4c7c-a26d-f4663d63cb3d	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	29c21f33-418d-463f-9c21-673daf5c933c	t	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795108+05:30	2026-08-18 11:23:08.795111+05:30
19025658-027a-4787-847b-4a16d4b12eee	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	5cad4a15-9a33-4d23-bf15-44bdb2935137	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795131+05:30	2026-08-18 11:23:08.795202+05:30
bf50cbf6-c618-4778-9573-662a8d90d65d	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	ebd081c5-b2ef-489c-aa2b-a833762733ba	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795241+05:30	2026-08-18 11:23:08.795245+05:30
fd36eeee-72d6-419b-9e82-6a13b1625bf0	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	2f4c3200-b45f-4482-b2f1-7cc9e71033f0	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795264+05:30	2026-08-18 11:23:08.795268+05:30
f50d943a-b8a7-49e7-b65c-7387d3a5b6d9	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	df60e01d-a5dd-4e71-b666-957bc465b8cb	t	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795285+05:30	2026-08-18 11:23:08.795289+05:30
0f783c4d-14af-4ae6-9561-5ee09f5d526b	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	4386b6aa-672c-4c8a-b8ab-75b12bbe1236	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795307+05:30	2026-08-18 11:23:08.79531+05:30
419320c1-d74d-4f69-bc5c-153bc3015c28	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	08e7a6b3-71ff-4607-a7bd-dd663ae76bc0	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795328+05:30	2026-08-18 11:23:08.795332+05:30
39de9334-7153-4a72-bcf2-b57369e254a9	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	117216d0-d735-4552-92e5-ef498dd89274	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795349+05:30	2026-08-18 11:23:08.795352+05:30
47747a12-8629-4e2a-951d-3477c438b422	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	c08c17d7-9437-4935-b6d1-f3ef453b4271	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795369+05:30	2026-08-18 11:23:08.795372+05:30
64db979b-b270-4619-b911-abe221a87238	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	b45f435c-2c5f-4db1-bfdc-18d99e1c61f2	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795389+05:30	2026-08-18 11:23:08.795393+05:30
9238f616-f268-4398-a72d-1725c57e9a0c	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	50a5640b-0177-4e2c-abd2-48380d37a5f3	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795409+05:30	2026-08-18 11:23:08.795411+05:30
c73aa178-6f5b-46d1-9cd4-750146ce8ab7	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	0d363f6a-68be-4f7b-811e-c49947613d28	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795431+05:30	2026-08-18 11:23:08.795435+05:30
996a4ef9-2e78-4080-bbc1-9388e92a7378	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	3687ff57-9933-4113-9776-b314dc96a36f	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795452+05:30	2026-08-18 11:23:08.795455+05:30
e7a4f291-ae55-48a3-b585-24766ff71384	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	ccc5fd17-3f4c-47d1-86b5-ea2d5e2dd6df	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795472+05:30	2026-08-18 11:23:08.795475+05:30
f4a129e0-8f26-471a-8920-ed04002f259f	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	79978747-b2bd-4a7f-a198-0a5407d835f7	t	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795491+05:30	2026-08-18 11:23:08.795494+05:30
9b9858e1-b8a6-4e6c-965d-d923d9fcbd07	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	4ef4f388-0729-4097-9ff6-a1e0a0aece56	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795511+05:30	2026-08-18 11:23:08.795515+05:30
77a33aad-3ebc-4e94-a00e-16016ef35de9	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	6c12994d-1a18-477b-a8a4-876c9d638654	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795532+05:30	2026-08-18 11:23:08.795535+05:30
48a3e62c-13d1-4da7-864c-0c223676e4e3	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	3ec3a864-19d8-4d55-b49e-8f75247eb549	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795552+05:30	2026-08-18 11:23:08.795555+05:30
31f1656a-b885-4659-a830-7deb72d99605	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	0f3dde44-f08a-4066-bfbd-b6872e0d67c9	t	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795572+05:30	2026-08-18 11:23:08.795575+05:30
03b72d5e-fd9d-4f7a-9cc8-2450fc33afce	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	68ea5a2e-4581-42f2-8e95-b1fb6a528ae7	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795592+05:30	2026-08-18 11:23:08.795596+05:30
bbd52261-275e-436f-97b4-d4c02202a113	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	ef7b1fba-8f81-4f8d-bd7a-81c26e1184ce	t	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795615+05:30	2026-08-18 11:23:08.795617+05:30
eff3b502-dc94-4faa-86b0-2ab7e191b982	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	218274c6-e131-4153-83a3-18f49d1f009d	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795636+05:30	2026-08-18 11:23:08.795639+05:30
8f46afe4-d3f1-474b-add0-ab6a5c3322b4	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	4d17caeb-67fa-40c3-8f87-99d0d9b672fa	t	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795656+05:30	2026-08-18 11:23:08.79566+05:30
68e95766-7113-4a9d-80ad-b701ceee20c8	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	176ec945-4da5-400d-9a8b-4ddf2e2b5b4b	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795678+05:30	2026-08-18 11:23:08.795681+05:30
d6745348-6445-4dfe-94ce-41fa9ff0ae7d	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	687f5223-3b75-4fa9-89e9-ab2aecd8acf8	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795699+05:30	2026-08-18 11:23:08.795702+05:30
d35af8de-98e5-46fa-9431-6df20eb3fdad	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	b321edbd-3b91-4d19-ac86-d5f78fff83a7	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795718+05:30	2026-08-18 11:23:08.795722+05:30
053faa94-fc66-4cab-ae5d-a7cb5c7a2bfb	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	4fdb5bb7-383b-4e1e-8e04-e8397db1a0d5	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795738+05:30	2026-08-18 11:23:08.795741+05:30
4fb86e56-cced-435b-9db1-0420df219700	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	2bcc4420-6cfa-4477-9700-118f1ce4b3a1	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795758+05:30	2026-08-18 11:23:08.795761+05:30
7c29861d-528e-439d-9e9f-41ea5b7a06c3	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	830d8388-0cb5-4d32-aa5e-a3f4858b73c0	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795778+05:30	2026-08-18 11:23:08.795782+05:30
885a3655-d7b7-4152-832e-415edf8852ae	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	f62fe28e-3cf4-414d-a85a-cb53d42632f9	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795801+05:30	2026-08-18 11:23:08.795805+05:30
d5286137-18c3-4a8b-a173-387fb403b3c0	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	f743a660-162d-450e-bafc-a9bb900b93d2	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795821+05:30	2026-08-18 11:23:08.795824+05:30
3b35f4ec-93b2-4b75-980e-8838631a2ac7	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	27751110-600e-4c3a-a280-58715c9ecb57	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795841+05:30	2026-08-18 11:23:08.795844+05:30
9803c53c-ae3b-4a64-b452-ac81e1af15ea	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	86df68a7-8d5a-4638-a21b-37ee1389b5f7	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795859+05:30	2026-08-18 11:23:08.795862+05:30
dd830988-c644-42cd-b882-5ebc72bf8322	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	7cad19da-93d1-4932-87a1-2908b1f35d92	t	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795878+05:30	2026-08-18 11:23:08.795881+05:30
60faf615-50f1-45db-9f94-b30a8e6eb3b8	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	0ac5e123-1f2f-4cfc-b036-353a0b859c6c	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795897+05:30	2026-08-18 11:23:08.7959+05:30
415c94a5-b4a2-4548-b55a-c52f2ccc8713	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	a051f70f-7c0a-48fe-824a-4d7b7d4691b3	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795916+05:30	2026-08-18 11:23:08.79592+05:30
6cf4d51f-b843-4034-abc9-afd6204ae3ca	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	fe680993-c2bd-4d0c-b081-a6af1a047f31	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795935+05:30	2026-08-18 11:23:08.795938+05:30
77da6cd5-5e8a-4dcc-a4da-9e43061449f3	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	1dc570b2-aa15-47fe-9a47-d93585ca8f7a	t	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795954+05:30	2026-08-18 11:23:08.795957+05:30
2a01ffb1-09e7-428d-972d-19e49f2c864c	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	7300be74-ce98-477e-bcdd-f945699e8039	t	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795017+05:30	2026-08-18 16:53:01.841895+05:30
e667b35a-6411-4b13-97c1-b46ddb3c26f1	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	df77f086-b3b2-45b0-a013-c8153f748d03	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795992+05:30	2026-08-18 11:23:08.795996+05:30
386f6bc2-e53f-4beb-bf6a-f6f1464a4134	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	71d8eb7d-62d2-4e31-85d4-0f0e7cb11290	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.796037+05:30	2026-08-18 11:23:08.796058+05:30
6b28499b-0396-49bf-8174-3fe9fdbc7c92	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	b5e273f7-c4b7-4dbd-9de4-66f821a4fafe	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.7961+05:30	2026-08-18 11:23:08.796104+05:30
14c1a38d-aec3-4e49-aa86-537e8f77fe23	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	abca03e3-5130-4400-b711-78aac0d16b51	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.796123+05:30	2026-08-18 11:23:08.796126+05:30
3f1e5b29-6e2d-4e56-80be-673d9f328308	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	99d73b40-034a-4813-bdeb-48a6b90550c8	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.796165+05:30	2026-08-18 11:23:08.796169+05:30
16ce4de4-fa87-4375-8f67-7f2b1dc90c71	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	e0a8705e-7c3b-4076-988e-e8d3f3bc78b4	t	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.796189+05:30	2026-08-18 11:23:08.796192+05:30
6136de40-e03b-4bf2-a0b6-cbc581de386b	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	ef177366-dee5-4be4-b9dc-0693181cc91b	f	t	t	0.7	10	Real-time	CPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.796209+05:30	2026-08-18 11:23:08.796212+05:30
b9f1fc76-e6ba-428e-8697-c4854026227b	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	5a761f99-4405-4d3f-9bf0-b25e1a68322a	t	t	t	0.7	10	Real-time	CPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.796228+05:30	2026-08-18 11:23:08.796231+05:30
c8baebdd-70df-4134-b74e-2130bc877a23	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	1ebcb63c-5fc5-4838-99fa-963e909d8512	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.796248+05:30	2026-08-18 11:23:08.796252+05:30
fe2ebae2-e396-435b-a06a-acca4e985d0a	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	ba091ec7-9a0e-42de-a349-0954db03e072	t	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950007+05:30	2026-08-18 12:30:08.950019+05:30
80b5fc12-db1b-482a-a774-09283ee911ea	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	7300be74-ce98-477e-bcdd-f945699e8039	t	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950044+05:30	2026-08-18 12:30:08.950047+05:30
82d65436-58c4-46b5-9459-7e74d6e13ddf	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	6ddef5a8-df19-4b35-8b41-2d3a46d73af9	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950063+05:30	2026-08-18 12:30:08.950065+05:30
884c33be-370b-4d3d-b722-491a62a97c6a	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	0754c127-34f5-48ea-8e9a-0d4de67ba813	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950079+05:30	2026-08-18 12:30:08.950081+05:30
5dd57c8f-79e5-4293-ba49-32eda7e00a42	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	305f9726-81b8-49f5-b7be-d1f80053ff3b	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950096+05:30	2026-08-18 12:30:08.950099+05:30
f2012e16-5541-4b34-b0e7-d539d446f595	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	29c21f33-418d-463f-9c21-673daf5c933c	t	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950112+05:30	2026-08-18 12:30:08.950114+05:30
768fdc8c-54d8-4fec-9c14-24a9c2f2ef11	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	5cad4a15-9a33-4d23-bf15-44bdb2935137	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950127+05:30	2026-08-18 12:30:08.950129+05:30
5b4a4613-81e9-4ce5-a268-ad39aae757f6	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	ebd081c5-b2ef-489c-aa2b-a833762733ba	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950163+05:30	2026-08-18 12:30:08.950181+05:30
39830a6f-e6d8-4aa4-b735-62517dc1d89a	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	2f4c3200-b45f-4482-b2f1-7cc9e71033f0	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950203+05:30	2026-08-18 12:30:08.950208+05:30
5634f275-cc6c-4d59-88f3-8b6685fc3bb3	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	df60e01d-a5dd-4e71-b666-957bc465b8cb	t	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950232+05:30	2026-08-18 12:30:08.950236+05:30
3d04076d-8d6f-460b-bcb4-741f61c9cf44	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	4386b6aa-672c-4c8a-b8ab-75b12bbe1236	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.95026+05:30	2026-08-18 12:30:08.950265+05:30
eabff193-7228-444c-bb0c-b8f600bba7d0	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	08e7a6b3-71ff-4607-a7bd-dd663ae76bc0	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950278+05:30	2026-08-18 12:30:08.950281+05:30
006ae46e-2354-411f-a9d5-d472fe18215d	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	117216d0-d735-4552-92e5-ef498dd89274	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950305+05:30	2026-08-18 12:30:08.950308+05:30
419ed79c-60df-4e12-b180-75bd74062f53	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	c08c17d7-9437-4935-b6d1-f3ef453b4271	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950321+05:30	2026-08-18 12:30:08.950323+05:30
157f75ed-095a-4bdc-9674-8e641dfcd586	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	b45f435c-2c5f-4db1-bfdc-18d99e1c61f2	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950339+05:30	2026-08-18 12:30:08.950341+05:30
5aae8136-d468-45de-91b6-36b7668594f3	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	50a5640b-0177-4e2c-abd2-48380d37a5f3	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950356+05:30	2026-08-18 12:30:08.950359+05:30
67b020f2-40bb-4367-9ad2-c98b6e49606b	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	0d363f6a-68be-4f7b-811e-c49947613d28	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950373+05:30	2026-08-18 12:30:08.950376+05:30
5ef5aa07-de1a-40bb-a87f-f04e4af42bf8	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	3687ff57-9933-4113-9776-b314dc96a36f	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950389+05:30	2026-08-18 12:30:08.950391+05:30
50a80511-eaa8-498a-a364-81242107629c	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	ccc5fd17-3f4c-47d1-86b5-ea2d5e2dd6df	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950404+05:30	2026-08-18 12:30:08.950407+05:30
4becbe9d-3fab-429a-b59f-5264e7426895	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	79978747-b2bd-4a7f-a198-0a5407d835f7	t	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.95042+05:30	2026-08-18 12:30:08.950423+05:30
0042a805-abd9-4025-8256-f79d1400ed64	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	4ef4f388-0729-4097-9ff6-a1e0a0aece56	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950436+05:30	2026-08-18 12:30:08.950438+05:30
3f638a88-3b5b-4655-b983-ba31bfaf91ac	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	6c12994d-1a18-477b-a8a4-876c9d638654	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950451+05:30	2026-08-18 12:30:08.950454+05:30
970bf25d-0b91-4fc6-b4cb-25426ebe26b1	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	3ec3a864-19d8-4d55-b49e-8f75247eb549	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950468+05:30	2026-08-18 12:30:08.950471+05:30
0236153f-bb48-4134-a24f-4ee42e438abb	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	0f3dde44-f08a-4066-bfbd-b6872e0d67c9	t	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950483+05:30	2026-08-18 12:30:08.950486+05:30
99b8849d-a4f9-43ea-8ed1-c15389982c57	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	68ea5a2e-4581-42f2-8e95-b1fb6a528ae7	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950499+05:30	2026-08-18 12:30:08.950501+05:30
047dcd98-35c5-4091-9573-000584d073d9	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	ef7b1fba-8f81-4f8d-bd7a-81c26e1184ce	t	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950514+05:30	2026-08-18 12:30:08.950516+05:30
4aa8e4cb-ad79-41b6-b5d6-75f2a990d77f	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	218274c6-e131-4153-83a3-18f49d1f009d	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950529+05:30	2026-08-18 12:30:08.950532+05:30
b956525e-80dc-4c14-ba27-856659ace852	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	4d17caeb-67fa-40c3-8f87-99d0d9b672fa	t	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950545+05:30	2026-08-18 12:30:08.950547+05:30
13843d6d-2bff-4b45-ab9c-cb61161da5fd	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	176ec945-4da5-400d-9a8b-4ddf2e2b5b4b	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950561+05:30	2026-08-18 12:30:08.950563+05:30
bc09f10f-a84f-432e-824d-a373c386dade	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	687f5223-3b75-4fa9-89e9-ab2aecd8acf8	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950576+05:30	2026-08-18 12:30:08.950579+05:30
b177015b-913e-4ec9-9b0b-2d297fae627e	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	b321edbd-3b91-4d19-ac86-d5f78fff83a7	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950593+05:30	2026-08-18 12:30:08.950596+05:30
74a587d1-d9f6-4652-a6f5-8d8a7e60293a	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	4fdb5bb7-383b-4e1e-8e04-e8397db1a0d5	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950609+05:30	2026-08-18 12:30:08.950612+05:30
5cbdf1d3-0d33-472f-953d-8eaf5281a9ee	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	cc8bac03-c480-4d02-a052-357889a6ad1d	t	t	t	0.7	10	Real-time	CPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.79608+05:30	2026-08-18 17:02:32.457673+05:30
d7761944-b857-469f-8429-0c87ca28df4d	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	2bcc4420-6cfa-4477-9700-118f1ce4b3a1	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950624+05:30	2026-08-18 12:30:08.950627+05:30
51c5e24c-0f77-43cf-8d07-1da37c518609	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	830d8388-0cb5-4d32-aa5e-a3f4858b73c0	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950641+05:30	2026-08-18 12:30:08.950643+05:30
6193ae2c-8257-4ae7-b72a-9e0ecd109f20	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	f62fe28e-3cf4-414d-a85a-cb53d42632f9	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950657+05:30	2026-08-18 12:30:08.950659+05:30
ac24edfb-4756-4efa-95f7-865485cc4e9a	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	f743a660-162d-450e-bafc-a9bb900b93d2	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950672+05:30	2026-08-18 12:30:08.950674+05:30
0c1b643c-19ba-45cf-8daf-5931d5d1fcf8	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	27751110-600e-4c3a-a280-58715c9ecb57	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950687+05:30	2026-08-18 12:30:08.950689+05:30
a72c6963-0a78-4d4c-8c6b-25e1e3c4779f	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	86df68a7-8d5a-4638-a21b-37ee1389b5f7	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950704+05:30	2026-08-18 12:30:08.950706+05:30
4a6b78a3-d250-4459-80ae-c5b4e46c8262	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	7cad19da-93d1-4932-87a1-2908b1f35d92	t	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950719+05:30	2026-08-18 12:30:08.950721+05:30
1d8ed58c-a736-493f-8c16-5b041a191f2a	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	0ac5e123-1f2f-4cfc-b036-353a0b859c6c	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950734+05:30	2026-08-18 12:30:08.950736+05:30
151931ab-0215-4c5a-ab98-76f4c8730114	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	a051f70f-7c0a-48fe-824a-4d7b7d4691b3	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.95075+05:30	2026-08-18 12:30:08.950752+05:30
fb24e249-b4c6-41c2-9e64-efb605fe505e	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	fe680993-c2bd-4d0c-b081-a6af1a047f31	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950766+05:30	2026-08-18 12:30:08.950769+05:30
89259b34-efc2-4404-b2b1-7d50d3a2ac72	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	1dc570b2-aa15-47fe-9a47-d93585ca8f7a	t	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950782+05:30	2026-08-18 12:30:08.950785+05:30
9a6a0a33-eeb6-4036-91a1-c7525eb8289b	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	303d2ead-f447-47b9-be02-68c18a9ee517	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950797+05:30	2026-08-18 12:30:08.9508+05:30
4285ee29-4ae4-499d-a1df-5af1a9fbd7c3	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	df77f086-b3b2-45b0-a013-c8153f748d03	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950812+05:30	2026-08-18 12:30:08.950814+05:30
6bebd509-e8b7-4a17-9d0a-06a218c0279d	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	71d8eb7d-62d2-4e31-85d4-0f0e7cb11290	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950828+05:30	2026-08-18 12:30:08.950831+05:30
bf36bfc7-d517-448c-9253-6a9f114d9558	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	cc8bac03-c480-4d02-a052-357889a6ad1d	f	t	t	0.7	10	Real-time	CPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950845+05:30	2026-08-18 12:30:08.950847+05:30
587558d7-3a6c-407c-83ee-f38fc616cdf2	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	b5e273f7-c4b7-4dbd-9de4-66f821a4fafe	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.95086+05:30	2026-08-18 12:30:08.950862+05:30
23af8008-7fef-43fa-a43d-e9f6dac5fb0b	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	abca03e3-5130-4400-b711-78aac0d16b51	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950875+05:30	2026-08-18 12:30:08.950877+05:30
3fada806-ae6b-4f42-b914-48bfed74c816	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	99d73b40-034a-4813-bdeb-48a6b90550c8	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950889+05:30	2026-08-18 12:30:08.950892+05:30
391cda32-f580-4748-b904-f948eb7fc892	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	e0a8705e-7c3b-4076-988e-e8d3f3bc78b4	t	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950904+05:30	2026-08-18 12:30:08.950907+05:30
5eac48a2-8ab2-4946-b4d5-262335d04faf	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	ef177366-dee5-4be4-b9dc-0693181cc91b	f	t	t	0.7	10	Real-time	CPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.95092+05:30	2026-08-18 12:30:08.950922+05:30
569dff42-79d5-4752-a13d-0c47798b3b66	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	5a761f99-4405-4d3f-9bf0-b25e1a68322a	t	t	t	0.7	10	Real-time	CPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950937+05:30	2026-08-18 12:30:08.950939+05:30
d2542280-4b07-42b0-8f92-dc448a95ef71	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	1ebcb63c-5fc5-4838-99fa-963e909d8512	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 12:30:08.950952+05:30	2026-08-18 12:30:08.950954+05:30
a902a247-10cc-4484-8bed-9beaa42233e9	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	303d2ead-f447-47b9-be02-68c18a9ee517	t	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.795973+05:30	2026-08-18 16:02:18.187881+05:30
73460236-593c-4876-bba7-67001592e7c9	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	ba091ec7-9a0e-42de-a349-0954db03e072	f	t	t	0.7	10	Real-time	GPU	t	30	{"auto_action": "ALERT", "roi_enabled": false}	2026-08-18 11:23:08.794964+05:30	2026-08-18 23:05:13.428682+05:30
\.


--
-- Data for Name: organizations; Type: TABLE DATA; Schema: public; Owner: kirti
--

COPY public.organizations (id, name, slug, is_active, created_at, updated_at) FROM stdin;
983e6cd6-65c7-4146-beb3-16df7bbd2ce5	Default Security Corp	default-corp	t	2026-08-18 11:23:08.427114+05:30	2026-08-18 11:23:08.427122+05:30
d0733e3d-5df3-4b3e-b399-201ec7a8eebf	foundit	foundit	t	2026-08-18 12:30:08.866577+05:30	2026-08-18 12:30:08.866609+05:30
\.


--
-- Data for Name: parameter_camera_assignments; Type: TABLE DATA; Schema: public; Owner: kirti
--

COPY public.parameter_camera_assignments (id, organization_id, camera_id, parameter_id, enabled, created_at) FROM stdin;
\.


--
-- Data for Name: permissions; Type: TABLE DATA; Schema: public; Owner: kirti
--

COPY public.permissions (id, code, module, description) FROM stdin;
\.


--
-- Data for Name: persons; Type: TABLE DATA; Schema: public; Owner: kirti
--

COPY public.persons (id, tenant_id, external_id, full_name, department, access_level, is_blacklisted, is_active, created_at, updated_at) FROM stdin;
bd46806d-d06d-4280-9018-4a351b12dbd2	e5940184-3c6c-4ae0-907b-e4f040336e7b	EMP-116321	kirti rani	General	STANDARD	t	t	2026-08-18 12:14:18.911216+05:30	2026-08-18 12:14:18.911247+05:30
\.


--
-- Data for Name: recordings; Type: TABLE DATA; Schema: public; Owner: kirti
--

COPY public.recordings (id, camera_id, file_path, file_size_bytes, duration_seconds, start_time, end_time) FROM stdin;
\.


--
-- Data for Name: role_permissions; Type: TABLE DATA; Schema: public; Owner: kirti
--

COPY public.role_permissions (role_id, permission_id) FROM stdin;
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: kirti
--

COPY public.roles (id, tenant_id, name, description, is_system) FROM stdin;
77c4b099-cff4-412b-af44-57f845b5ca1e	\N	SUPER_ADMIN	System Super Admin	t
08a7fb4f-0744-42f0-a01f-0281227286ec	\N	OPERATOR	Security Command Center Operator	t
\.


--
-- Data for Name: tenants; Type: TABLE DATA; Schema: public; Owner: kirti
--

COPY public.tenants (id, organization_id, name, code, config, is_active, created_at, updated_at) FROM stdin;
e5940184-3c6c-4ae0-907b-e4f040336e7b	983e6cd6-65c7-4146-beb3-16df7bbd2ce5	HQ Security Campus	hq-campus	{"max_cameras": 100, "ai_features": ["FACE", "YOLO", "OCR", "ENHANCE"]}	t	2026-08-18 11:23:08.432198+05:30	2026-08-18 11:23:08.43221+05:30
c6b57e32-3e73-4869-8999-72fbb78b6318	d0733e3d-5df3-4b3e-b399-201ec7a8eebf	foundit Main HQ	foundit-hq	{"max_cameras": 50}	t	2026-08-18 12:30:08.879234+05:30	2026-08-18 12:30:08.879255+05:30
\.


--
-- Data for Name: user_roles; Type: TABLE DATA; Schema: public; Owner: kirti
--

COPY public.user_roles (user_id, role_id) FROM stdin;
3f0e93db-2dba-4ee8-bd70-86903ef893f6	77c4b099-cff4-412b-af44-57f845b5ca1e
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: kirti
--

COPY public.users (id, tenant_id, email, password_hash, full_name, is_superuser, is_active, created_at, updated_at) FROM stdin;
3f0e93db-2dba-4ee8-bd70-86903ef893f6	e5940184-3c6c-4ae0-907b-e4f040336e7b	admin@sentriqvision.com	$2b$12$gJuZIHwe3FpykbPw4wvJ9OBnwg6WENlIyR/Gejji226K4Ug2Wy82K	System Administrator	t	t	2026-08-18 11:23:08.733068+05:30	2026-08-18 11:23:08.733074+05:30
\.


--
-- Name: ai_inference_logs pk_ai_inference_logs; Type: CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.ai_inference_logs
    ADD CONSTRAINT pk_ai_inference_logs PRIMARY KEY (id);


--
-- Name: ai_parameter_catalog pk_ai_parameter_catalog; Type: CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.ai_parameter_catalog
    ADD CONSTRAINT pk_ai_parameter_catalog PRIMARY KEY (id);


--
-- Name: alert_rules pk_alert_rules; Type: CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.alert_rules
    ADD CONSTRAINT pk_alert_rules PRIMARY KEY (id);


--
-- Name: alerts pk_alerts; Type: CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.alerts
    ADD CONSTRAINT pk_alerts PRIMARY KEY (id);


--
-- Name: audit_logs pk_audit_logs; Type: CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT pk_audit_logs PRIMARY KEY (id);


--
-- Name: camera_health pk_camera_health; Type: CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.camera_health
    ADD CONSTRAINT pk_camera_health PRIMARY KEY (id);


--
-- Name: cameras pk_cameras; Type: CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.cameras
    ADD CONSTRAINT pk_cameras PRIMARY KEY (id);


--
-- Name: event_frames pk_event_frames; Type: CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.event_frames
    ADD CONSTRAINT pk_event_frames PRIMARY KEY (id);


--
-- Name: events pk_events; Type: CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT pk_events PRIMARY KEY (id);


--
-- Name: face_embeddings pk_face_embeddings; Type: CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.face_embeddings
    ADD CONSTRAINT pk_face_embeddings PRIMARY KEY (id);


--
-- Name: organization_ai_parameters pk_organization_ai_parameters; Type: CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.organization_ai_parameters
    ADD CONSTRAINT pk_organization_ai_parameters PRIMARY KEY (id);


--
-- Name: organizations pk_organizations; Type: CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT pk_organizations PRIMARY KEY (id);


--
-- Name: parameter_camera_assignments pk_parameter_camera_assignments; Type: CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.parameter_camera_assignments
    ADD CONSTRAINT pk_parameter_camera_assignments PRIMARY KEY (id);


--
-- Name: permissions pk_permissions; Type: CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT pk_permissions PRIMARY KEY (id);


--
-- Name: persons pk_persons; Type: CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.persons
    ADD CONSTRAINT pk_persons PRIMARY KEY (id);


--
-- Name: recordings pk_recordings; Type: CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.recordings
    ADD CONSTRAINT pk_recordings PRIMARY KEY (id);


--
-- Name: role_permissions pk_role_permissions; Type: CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT pk_role_permissions PRIMARY KEY (role_id, permission_id);


--
-- Name: roles pk_roles; Type: CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT pk_roles PRIMARY KEY (id);


--
-- Name: tenants pk_tenants; Type: CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.tenants
    ADD CONSTRAINT pk_tenants PRIMARY KEY (id);


--
-- Name: user_roles pk_user_roles; Type: CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT pk_user_roles PRIMARY KEY (user_id, role_id);


--
-- Name: users pk_users; Type: CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT pk_users PRIMARY KEY (id);


--
-- Name: organization_ai_parameters uq_org_parameter; Type: CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.organization_ai_parameters
    ADD CONSTRAINT uq_org_parameter UNIQUE (organization_id, parameter_id);


--
-- Name: parameter_camera_assignments uq_param_cam_assignment; Type: CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.parameter_camera_assignments
    ADD CONSTRAINT uq_param_cam_assignment UNIQUE (organization_id, camera_id, parameter_id);


--
-- Name: ix_ai_inference_logs_camera_id; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_ai_inference_logs_camera_id ON public.ai_inference_logs USING btree (camera_id);


--
-- Name: ix_ai_inference_logs_created_at; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_ai_inference_logs_created_at ON public.ai_inference_logs USING btree (created_at);


--
-- Name: ix_ai_inference_logs_organization_id; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_ai_inference_logs_organization_id ON public.ai_inference_logs USING btree (organization_id);


--
-- Name: ix_ai_inference_logs_parameter_code; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_ai_inference_logs_parameter_code ON public.ai_inference_logs USING btree (parameter_code);


--
-- Name: ix_ai_parameter_catalog_code; Type: INDEX; Schema: public; Owner: kirti
--

CREATE UNIQUE INDEX ix_ai_parameter_catalog_code ON public.ai_parameter_catalog USING btree (code);


--
-- Name: ix_ai_parameter_catalog_domain; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_ai_parameter_catalog_domain ON public.ai_parameter_catalog USING btree (domain);


--
-- Name: ix_ai_parameter_catalog_service_number; Type: INDEX; Schema: public; Owner: kirti
--

CREATE UNIQUE INDEX ix_ai_parameter_catalog_service_number ON public.ai_parameter_catalog USING btree (service_number);


--
-- Name: ix_alert_rules_tenant_id; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_alert_rules_tenant_id ON public.alert_rules USING btree (tenant_id);


--
-- Name: ix_alerts_created_at; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_alerts_created_at ON public.alerts USING btree (created_at);


--
-- Name: ix_alerts_event_id; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_alerts_event_id ON public.alerts USING btree (event_id);


--
-- Name: ix_alerts_rule_id; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_alerts_rule_id ON public.alerts USING btree (rule_id);


--
-- Name: ix_alerts_severity; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_alerts_severity ON public.alerts USING btree (severity);


--
-- Name: ix_alerts_status; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_alerts_status ON public.alerts USING btree (status);


--
-- Name: ix_alerts_tenant_id; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_alerts_tenant_id ON public.alerts USING btree (tenant_id);


--
-- Name: ix_audit_logs_action; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_audit_logs_action ON public.audit_logs USING btree (action);


--
-- Name: ix_audit_logs_created_at; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_audit_logs_created_at ON public.audit_logs USING btree (created_at);


--
-- Name: ix_audit_logs_organization_id; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_audit_logs_organization_id ON public.audit_logs USING btree (organization_id);


--
-- Name: ix_audit_logs_user_id; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_audit_logs_user_id ON public.audit_logs USING btree (user_id);


--
-- Name: ix_camera_health_camera_id; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_camera_health_camera_id ON public.camera_health USING btree (camera_id);


--
-- Name: ix_cameras_tenant_id; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_cameras_tenant_id ON public.cameras USING btree (tenant_id);


--
-- Name: ix_event_frames_event_id; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_event_frames_event_id ON public.event_frames USING btree (event_id);


--
-- Name: ix_events_camera_id; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_events_camera_id ON public.events USING btree (camera_id);


--
-- Name: ix_events_event_type; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_events_event_type ON public.events USING btree (event_type);


--
-- Name: ix_events_severity; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_events_severity ON public.events USING btree (severity);


--
-- Name: ix_events_tenant_id; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_events_tenant_id ON public.events USING btree (tenant_id);


--
-- Name: ix_events_timestamp; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_events_timestamp ON public.events USING btree ("timestamp");


--
-- Name: ix_face_embeddings_person_id; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_face_embeddings_person_id ON public.face_embeddings USING btree (person_id);


--
-- Name: ix_organization_ai_parameters_organization_id; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_organization_ai_parameters_organization_id ON public.organization_ai_parameters USING btree (organization_id);


--
-- Name: ix_organization_ai_parameters_parameter_id; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_organization_ai_parameters_parameter_id ON public.organization_ai_parameters USING btree (parameter_id);


--
-- Name: ix_organizations_slug; Type: INDEX; Schema: public; Owner: kirti
--

CREATE UNIQUE INDEX ix_organizations_slug ON public.organizations USING btree (slug);


--
-- Name: ix_parameter_camera_assignments_camera_id; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_parameter_camera_assignments_camera_id ON public.parameter_camera_assignments USING btree (camera_id);


--
-- Name: ix_parameter_camera_assignments_organization_id; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_parameter_camera_assignments_organization_id ON public.parameter_camera_assignments USING btree (organization_id);


--
-- Name: ix_parameter_camera_assignments_parameter_id; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_parameter_camera_assignments_parameter_id ON public.parameter_camera_assignments USING btree (parameter_id);


--
-- Name: ix_permissions_code; Type: INDEX; Schema: public; Owner: kirti
--

CREATE UNIQUE INDEX ix_permissions_code ON public.permissions USING btree (code);


--
-- Name: ix_persons_tenant_id; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_persons_tenant_id ON public.persons USING btree (tenant_id);


--
-- Name: ix_recordings_camera_id; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_recordings_camera_id ON public.recordings USING btree (camera_id);


--
-- Name: ix_roles_tenant_id; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_roles_tenant_id ON public.roles USING btree (tenant_id);


--
-- Name: ix_tenants_code; Type: INDEX; Schema: public; Owner: kirti
--

CREATE UNIQUE INDEX ix_tenants_code ON public.tenants USING btree (code);


--
-- Name: ix_tenants_organization_id; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_tenants_organization_id ON public.tenants USING btree (organization_id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: kirti
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_tenant_id; Type: INDEX; Schema: public; Owner: kirti
--

CREATE INDEX ix_users_tenant_id ON public.users USING btree (tenant_id);


--
-- Name: alert_rules fk_alert_rules_tenant_id_tenants; Type: FK CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.alert_rules
    ADD CONSTRAINT fk_alert_rules_tenant_id_tenants FOREIGN KEY (tenant_id) REFERENCES public.tenants(id) ON DELETE CASCADE;


--
-- Name: alerts fk_alerts_acknowledged_by_users; Type: FK CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.alerts
    ADD CONSTRAINT fk_alerts_acknowledged_by_users FOREIGN KEY (acknowledged_by) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: alerts fk_alerts_event_id_events; Type: FK CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.alerts
    ADD CONSTRAINT fk_alerts_event_id_events FOREIGN KEY (event_id) REFERENCES public.events(id) ON DELETE SET NULL;


--
-- Name: alerts fk_alerts_rule_id_alert_rules; Type: FK CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.alerts
    ADD CONSTRAINT fk_alerts_rule_id_alert_rules FOREIGN KEY (rule_id) REFERENCES public.alert_rules(id) ON DELETE SET NULL;


--
-- Name: alerts fk_alerts_tenant_id_tenants; Type: FK CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.alerts
    ADD CONSTRAINT fk_alerts_tenant_id_tenants FOREIGN KEY (tenant_id) REFERENCES public.tenants(id) ON DELETE CASCADE;


--
-- Name: camera_health fk_camera_health_camera_id_cameras; Type: FK CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.camera_health
    ADD CONSTRAINT fk_camera_health_camera_id_cameras FOREIGN KEY (camera_id) REFERENCES public.cameras(id) ON DELETE CASCADE;


--
-- Name: cameras fk_cameras_tenant_id_tenants; Type: FK CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.cameras
    ADD CONSTRAINT fk_cameras_tenant_id_tenants FOREIGN KEY (tenant_id) REFERENCES public.tenants(id) ON DELETE CASCADE;


--
-- Name: event_frames fk_event_frames_event_id_events; Type: FK CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.event_frames
    ADD CONSTRAINT fk_event_frames_event_id_events FOREIGN KEY (event_id) REFERENCES public.events(id) ON DELETE CASCADE;


--
-- Name: events fk_events_camera_id_cameras; Type: FK CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT fk_events_camera_id_cameras FOREIGN KEY (camera_id) REFERENCES public.cameras(id) ON DELETE SET NULL;


--
-- Name: events fk_events_tenant_id_tenants; Type: FK CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT fk_events_tenant_id_tenants FOREIGN KEY (tenant_id) REFERENCES public.tenants(id) ON DELETE CASCADE;


--
-- Name: face_embeddings fk_face_embeddings_person_id_persons; Type: FK CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.face_embeddings
    ADD CONSTRAINT fk_face_embeddings_person_id_persons FOREIGN KEY (person_id) REFERENCES public.persons(id) ON DELETE CASCADE;


--
-- Name: organization_ai_parameters fk_organization_ai_parameters_organization_id_organizations; Type: FK CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.organization_ai_parameters
    ADD CONSTRAINT fk_organization_ai_parameters_organization_id_organizations FOREIGN KEY (organization_id) REFERENCES public.organizations(id) ON DELETE CASCADE;


--
-- Name: organization_ai_parameters fk_organization_ai_parameters_parameter_id_ai_parameter_catalog; Type: FK CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.organization_ai_parameters
    ADD CONSTRAINT fk_organization_ai_parameters_parameter_id_ai_parameter_catalog FOREIGN KEY (parameter_id) REFERENCES public.ai_parameter_catalog(id) ON DELETE CASCADE;


--
-- Name: parameter_camera_assignments fk_parameter_camera_assignments_camera_id_cameras; Type: FK CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.parameter_camera_assignments
    ADD CONSTRAINT fk_parameter_camera_assignments_camera_id_cameras FOREIGN KEY (camera_id) REFERENCES public.cameras(id) ON DELETE CASCADE;


--
-- Name: parameter_camera_assignments fk_parameter_camera_assignments_organization_id_organizations; Type: FK CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.parameter_camera_assignments
    ADD CONSTRAINT fk_parameter_camera_assignments_organization_id_organizations FOREIGN KEY (organization_id) REFERENCES public.organizations(id) ON DELETE CASCADE;


--
-- Name: parameter_camera_assignments fk_parameter_camera_assignments_parameter_id_ai_paramet_2952; Type: FK CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.parameter_camera_assignments
    ADD CONSTRAINT fk_parameter_camera_assignments_parameter_id_ai_paramet_2952 FOREIGN KEY (parameter_id) REFERENCES public.ai_parameter_catalog(id) ON DELETE CASCADE;


--
-- Name: persons fk_persons_tenant_id_tenants; Type: FK CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.persons
    ADD CONSTRAINT fk_persons_tenant_id_tenants FOREIGN KEY (tenant_id) REFERENCES public.tenants(id) ON DELETE CASCADE;


--
-- Name: recordings fk_recordings_camera_id_cameras; Type: FK CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.recordings
    ADD CONSTRAINT fk_recordings_camera_id_cameras FOREIGN KEY (camera_id) REFERENCES public.cameras(id) ON DELETE CASCADE;


--
-- Name: role_permissions fk_role_permissions_permission_id_permissions; Type: FK CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT fk_role_permissions_permission_id_permissions FOREIGN KEY (permission_id) REFERENCES public.permissions(id) ON DELETE CASCADE;


--
-- Name: role_permissions fk_role_permissions_role_id_roles; Type: FK CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT fk_role_permissions_role_id_roles FOREIGN KEY (role_id) REFERENCES public.roles(id) ON DELETE CASCADE;


--
-- Name: roles fk_roles_tenant_id_tenants; Type: FK CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT fk_roles_tenant_id_tenants FOREIGN KEY (tenant_id) REFERENCES public.tenants(id) ON DELETE CASCADE;


--
-- Name: tenants fk_tenants_organization_id_organizations; Type: FK CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.tenants
    ADD CONSTRAINT fk_tenants_organization_id_organizations FOREIGN KEY (organization_id) REFERENCES public.organizations(id) ON DELETE CASCADE;


--
-- Name: user_roles fk_user_roles_role_id_roles; Type: FK CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT fk_user_roles_role_id_roles FOREIGN KEY (role_id) REFERENCES public.roles(id) ON DELETE CASCADE;


--
-- Name: user_roles fk_user_roles_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT fk_user_roles_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: users fk_users_tenant_id_tenants; Type: FK CONSTRAINT; Schema: public; Owner: kirti
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_users_tenant_id_tenants FOREIGN KEY (tenant_id) REFERENCES public.tenants(id) ON DELETE CASCADE;


--
-- Name: TABLE ai_inference_logs; Type: ACL; Schema: public; Owner: kirti
--

GRANT ALL ON TABLE public.ai_inference_logs TO sentriqvision;


--
-- Name: TABLE ai_parameter_catalog; Type: ACL; Schema: public; Owner: kirti
--

GRANT ALL ON TABLE public.ai_parameter_catalog TO sentriqvision;


--
-- Name: TABLE alert_rules; Type: ACL; Schema: public; Owner: kirti
--

GRANT ALL ON TABLE public.alert_rules TO sentriqvision;


--
-- Name: TABLE alerts; Type: ACL; Schema: public; Owner: kirti
--

GRANT ALL ON TABLE public.alerts TO sentriqvision;


--
-- Name: TABLE audit_logs; Type: ACL; Schema: public; Owner: kirti
--

GRANT ALL ON TABLE public.audit_logs TO sentriqvision;


--
-- Name: TABLE camera_health; Type: ACL; Schema: public; Owner: kirti
--

GRANT ALL ON TABLE public.camera_health TO sentriqvision;


--
-- Name: TABLE cameras; Type: ACL; Schema: public; Owner: kirti
--

GRANT ALL ON TABLE public.cameras TO sentriqvision;


--
-- Name: TABLE event_frames; Type: ACL; Schema: public; Owner: kirti
--

GRANT ALL ON TABLE public.event_frames TO sentriqvision;


--
-- Name: TABLE events; Type: ACL; Schema: public; Owner: kirti
--

GRANT ALL ON TABLE public.events TO sentriqvision;


--
-- Name: TABLE face_embeddings; Type: ACL; Schema: public; Owner: kirti
--

GRANT ALL ON TABLE public.face_embeddings TO sentriqvision;


--
-- Name: TABLE organization_ai_parameters; Type: ACL; Schema: public; Owner: kirti
--

GRANT ALL ON TABLE public.organization_ai_parameters TO sentriqvision;


--
-- Name: TABLE organizations; Type: ACL; Schema: public; Owner: kirti
--

GRANT ALL ON TABLE public.organizations TO sentriqvision;


--
-- Name: TABLE parameter_camera_assignments; Type: ACL; Schema: public; Owner: kirti
--

GRANT ALL ON TABLE public.parameter_camera_assignments TO sentriqvision;


--
-- Name: TABLE permissions; Type: ACL; Schema: public; Owner: kirti
--

GRANT ALL ON TABLE public.permissions TO sentriqvision;


--
-- Name: TABLE persons; Type: ACL; Schema: public; Owner: kirti
--

GRANT ALL ON TABLE public.persons TO sentriqvision;


--
-- Name: TABLE recordings; Type: ACL; Schema: public; Owner: kirti
--

GRANT ALL ON TABLE public.recordings TO sentriqvision;


--
-- Name: TABLE role_permissions; Type: ACL; Schema: public; Owner: kirti
--

GRANT ALL ON TABLE public.role_permissions TO sentriqvision;


--
-- Name: TABLE roles; Type: ACL; Schema: public; Owner: kirti
--

GRANT ALL ON TABLE public.roles TO sentriqvision;


--
-- Name: TABLE tenants; Type: ACL; Schema: public; Owner: kirti
--

GRANT ALL ON TABLE public.tenants TO sentriqvision;


--
-- Name: TABLE user_roles; Type: ACL; Schema: public; Owner: kirti
--

GRANT ALL ON TABLE public.user_roles TO sentriqvision;


--
-- Name: TABLE users; Type: ACL; Schema: public; Owner: kirti
--

GRANT ALL ON TABLE public.users TO sentriqvision;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON SEQUENCES TO sentriqvision;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON TABLES TO sentriqvision;


--
-- PostgreSQL database dump complete
--

\unrestrict vtMpnA82iU7pAQFOeJbklCk7B80Z3q8rYc0iFDnydV2uCTbfiSeoDVpFX1aXqL6

