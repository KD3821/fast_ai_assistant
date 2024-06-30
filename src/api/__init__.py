from fastapi import APIRouter

from .prompts import router as prompt_router
from .storage import router as storage_router

router = APIRouter()

router.include_router(prompt_router)
router.include_router(storage_router)
