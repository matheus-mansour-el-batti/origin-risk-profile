import logging

from fastapi import status
from fastapi.routing import APIRouter

from app.commons.logger import setup_logger
from app.schemas.request.risk_profile import RiskProfileInput
from app.services.risk_profile import RiskProfileService

setup_logger()
LOGGER = logging.getLogger(__name__)

risk_profile_router = APIRouter(prefix="/risk-profile")


@risk_profile_router.post("", status_code=status.HTTP_200_OK)
def risk_profile(data: RiskProfileInput):
    return RiskProfileService(data=data).get_risk_profile()
