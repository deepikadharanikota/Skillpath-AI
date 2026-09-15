import os
import redis.asyncio as redis
import json

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

async def set_session(session_id: str, user_id: int):
    await redis_client.set(f"session:{session_id}", user_id, ex=86400) # 1 day

async def get_session(session_id: str) -> int:
    user_id = await redis_client.get(f"session:{session_id}")
    return int(user_id) if user_id else None

async def delete_session(session_id: str):
    await redis_client.delete(f"session:{session_id}")
