import asyncio
import os

from fastapi import APIRouter, HTTPException, Query, status


demo_router = APIRouter(include_in_schema=False)


def _ensure_enabled() -> None:
    if os.getenv("SLI_DEMO_ENABLED", "false").lower() != "true":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@demo_router.get("/work")
async def demo_work(
    mode: str = Query(default="normal", pattern="^(normal|slow|error)$"),
):
    _ensure_enabled()
    if mode == "slow":
        await asyncio.sleep(float(os.getenv("SLI_DEMO_DELAY_SECONDS", "1.5")))
    elif mode == "error":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Synthetic SLI demo failure",
        )
    return {"status": "ok", "mode": mode}
