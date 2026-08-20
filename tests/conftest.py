import os
import sys
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

# Add backend directory to sys.path so app modules import cleanly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ["USE_SQLITE_FALLBACK"] = "True"
os.environ["SQLITE_DB_PATH"] = "./test_sentriqvision.db"

from app.core.database import AsyncSessionLocal, engine
from app.main import app
from app.models import Base
from app.services.auth_service import AuthService


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        auth_service = AuthService(session)
        await auth_service.seed_initial_data()

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
    if os.path.exists("./test_sentriqvision.db"):
        os.remove("./test_sentriqvision.db")


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
