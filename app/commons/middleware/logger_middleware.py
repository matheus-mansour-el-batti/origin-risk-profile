import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

LOGGER = logging.getLogger(__name__)


class LoggerMiddleware(BaseHTTPMiddleware):
    """
    Middleware that logs all requests
    """

    async def dispatch(self, request: Request, call_next):
        LOGGER.info(f'{request.method} on path {request.scope["path"]}')
        return await call_next(request)
