"""
Database Health Check
"""

from sqlalchemy import text

from app.database.session import engine



async def database_health():

    try:

        async with engine.connect() as conn:

            await conn.execute(
                text("SELECT 1")
            )


        return {
            "database": "healthy"
        }


    except Exception as e:

        return {

            "database": "unhealthy",

            "error": str(e)

        }