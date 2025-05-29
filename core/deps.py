from core.database import Session
from typing import Generator

async def get_session() -> Generator:
    session=  Session()
    try:
        yield session
    finally:
        await session.close()