from fastapi.routing import APIRouter

from .resources.base import index_router

router = APIRouter(prefix="", tags=["Application Index"])
router.include_router(index_router)
