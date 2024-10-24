from fastapi import APIRouter
from .claims_routes import router as claims_router

router = APIRouter(prefix="/v1")

router.include_router(claims_router, tags=["Claims"])