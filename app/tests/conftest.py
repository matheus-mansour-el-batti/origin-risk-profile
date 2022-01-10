import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.request.risk_profile import (
    House,
    MaritalStatus,
    OwnershipStatus,
    RiskProfileInput,
    Vehicle,
)
from app.services.risk_profile import RiskProfileService


@pytest.fixture()
def base_risk_profile_service_input():
    return RiskProfileService(
        data=RiskProfileInput(
            age=50,
            dependents=0,
            income=50000,
            marital_status=MaritalStatus.SINGLE,
            risk_questions=[0, 1, 1],
            house=House(ownership_status=OwnershipStatus.OWNED),
            vehicle=Vehicle(year=2010),
        )
    )


@pytest.fixture
def client():
    return TestClient(app)
