from fastapi import APIRouter
from .claims_routes import router as claims_router
from .users_routes import router as users_router
from .auth_routes import router as auth_router

router = APIRouter(prefix="/v1")

router.include_router(auth_router, tags=["Auth"])
router.include_router(claims_router, tags=["Claims"])
router.include_router(users_router, tags=["Users"])
