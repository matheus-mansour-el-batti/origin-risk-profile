from fastapi.routing import APIRouter

from .resources.risk_profile import risk_profile_router

router = APIRouter(prefix="/api/v1")
router.include_router(risk_profile_router, tags=["Risk Profile"])
