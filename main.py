import os

import redis.asyncio as redis
from fastapi import FastAPI

app = FastAPI()

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


@app.post("/hit/{key}")
async def hit(key: str):
    count = await redis_client.incr(key)
    return {"key": key, "count": count}


@app.get("/count/{key}")
async def count(key: str):
    value = await redis_client.get(key)
    return {"key": key, "count": int(value) if value is not None else 0}


@app.get("/healthz")
async def healthz():
    try:
        pong = await redis_client.ping()
        redis_status = "up" if pong else "down"
    except Exception:
        redis_status = "down"
    return {"status": "ok", "redis": redis_status}
