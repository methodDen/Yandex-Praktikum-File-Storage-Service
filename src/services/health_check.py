from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def ping_database(
    *,
    db: AsyncSession,
) -> bool:
    """Get database health status"""
    try:
        await db.execute(text("SELECT 1"))
    except (ConnectionRefusedError, Exception):
        return False
    return True
