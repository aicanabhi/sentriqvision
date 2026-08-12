from fastapi import FastAPI
from sqlalchemy import text
from app.config import settings
from app.database.connection import AsyncSessionLocal
# --------------------------------------------
# Create FastAPI application
# --------------------------------------------

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Enterprise CCTV AI Intelligence Platform",
)

# --------------------------------------------------------------
# Health Check
# --------------------------------------------------------------
# This is the first endpoint we create.
#
# Later Kubernetes/Docker/load balancers can use this endpoint
# to determine whether the API is alive.
# ---------------------------------------------------------------

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service":"platform-api",
        "version":settings.app_version,
    }

# --------------------------------------------------------------
# Root endpoint
# --------------------------------------------------------------
@app.get("/")
async def root():
    return {
        "message": "CCTV AI Platform API",
    }

@app.get("/health/database")
async def database_health_check():
    """
    Verify that the API can actually communicate with the PostgreSQL.
    """
    async with AsyncSessionLocal() as session:

        # Execute a trivial SQL query.
        result = await session.execute(text("SELECT 1"))

        #Extract the returned value.
        value = result.scalar_one()

    return {
        "status": "ok",
        "database": "postgresql",
        "query_result": value,
    }




