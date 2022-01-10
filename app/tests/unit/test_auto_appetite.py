import datetime

from app.schemas.response.risk_profile import InsuranceProfile
from app.services.risk_profile import RiskProfileService


def test_auto_risk_appetite__none_car_input(base_risk_profile_service_input):
    base_risk_profile_service_input.data.vehicle = None
    result = RiskProfileService.get_auto_risk_appetite(
        base_risk_profile_service_input, base_score=2
    )
    assert result.score is None
    assert result.profile == InsuranceProfile.INELIGIBLE


def test_auto_risk_appetite__base_risk_profile(base_risk_profile_service_input):
    result = RiskProfileService.get_auto_risk_appetite(
        base_risk_profile_service_input, base_score=2
    )
    assert result.score == 2
    assert result.profile == InsuranceProfile.REGULAR


def test_auto_risk_appetite__new_car(base_risk_profile_service_input):
    current_date = datetime.date.today()
    production_year = int(current_date.strftime("%Y")) - 2
    base_risk_profile_service_input.data.vehicle.year = (
        production_year  # Not hardcoding so test works forever
    )
    result = RiskProfileService.get_auto_risk_appetite(
        base_risk_profile_service_input, base_score=2
    )
    assert result.score == 3
    assert result.profile == InsuranceProfile.RESPONSIBLE


def test_auto_risk_appetite__high_income(base_risk_profile_service_input):
    base_risk_profile_service_input.data.income = 300000
    result = RiskProfileService.get_auto_risk_appetite(
        base_risk_profile_service_input, base_score=2
    )
    assert result.score == 1
    assert result.profile == InsuranceProfile.REGULAR


def test_auto_risk_appetite__very_low_age(base_risk_profile_service_input):
    base_risk_profile_service_input.data.age = 20
    result = RiskProfileService.get_auto_risk_appetite(
        base_risk_profile_service_input, base_score=2
    )
    assert result.score == 0
    assert result.profile == InsuranceProfile.ECONOMIC
