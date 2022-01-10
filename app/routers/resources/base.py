from fastapi.routing import APIRouter

index_router = APIRouter()


@index_router.get("/")
async def index():
    """
    Return Standard Application Running Message
    """
    return {"message": "Application Running", "docs": "/docs", "redoc": "/redoc"}
