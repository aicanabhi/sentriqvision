import asyncio

from app.infrastructure.database.mongodb import get_database
from app.infrastructure.security.hash import get_password_hash


async def reset_password():

    db = await get_database()

    password = "SuperAdmin123!"

    hashed_password = get_password_hash(password)

    result = await db.super_admin.update_one(
        {
            "email": "admin@sentriqvision.com"
        },
        {
            "$set": {
                "password": hashed_password
            }
        }
    )

    print("Matched:", result.matched_count)
    print("Modified:", result.modified_count)


asyncio.run(reset_password())