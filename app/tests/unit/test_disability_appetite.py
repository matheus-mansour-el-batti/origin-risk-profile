from app.schemas.request.risk_profile import MaritalStatus, OwnershipStatus
from app.schemas.response.risk_profile import InsuranceProfile
from app.services.risk_profile import RiskProfileService


def test_disability_risk_appetite_base_risk_profile(base_risk_profile_service_input):
    result = RiskProfileService.get_disability_risk_appetite(
        base_risk_profile_service_input, base_score=2
    )
    assert result.score == 2
    assert result.profile == InsuranceProfile.REGULAR


def test_disability_risk_appetite__none_income_input(base_risk_profile_service_input):
    base_risk_profile_service_input.data.income = 0
    result = RiskProfileService.get_disability_risk_appetite(
        base_risk_profile_service_input, base_score=2
    )
    assert result.score is None
    assert result.profile == InsuranceProfile.INELIGIBLE


def test_disability_risk_appetite__old_person(base_risk_profile_service_input):
    base_risk_profile_service_input.data.age = 61
    result = RiskProfileService.get_disability_risk_appetite(
        base_risk_profile_service_input, base_score=2
    )
    assert result.score is None
    assert result.profile == InsuranceProfile.INELIGIBLE


def test_disability_risk_appetite__mortgaged(base_risk_profile_service_input):
    base_risk_profile_service_input.data.house = OwnershipStatus.MORTGAGED
    result = RiskProfileService.get_disability_risk_appetite(
        base_risk_profile_service_input, base_score=2
    )
    assert result.score == 3
    assert result.profile == InsuranceProfile.RESPONSIBLE


def test_disability_risk_appetite__very_low_age(base_risk_profile_service_input):
    base_risk_profile_service_input.data.age = 20
    result = RiskProfileService.get_disability_risk_appetite(
        base_risk_profile_service_input, base_score=2
    )
    assert result.score == 0
    assert result.profile == InsuranceProfile.ECONOMIC


def test_disability_risk_appetite__high_income(base_risk_profile_service_input):
    base_risk_profile_service_input.data.income = 201000
    result = RiskProfileService.get_disability_risk_appetite(
        base_risk_profile_service_input, base_score=2
    )
    assert result.score == 1
    assert result.profile == InsuranceProfile.REGULAR


def test_disability_risk_appetite__married(base_risk_profile_service_input):
    base_risk_profile_service_input.data.marital_status = MaritalStatus.MARRIED
    result = RiskProfileService.get_disability_risk_appetite(
        base_risk_profile_service_input, base_score=2
    )
    assert result.score == 1
    assert result.profile == InsuranceProfile.REGULAR


def test_disability_risk_appetite__dependents(base_risk_profile_service_input):
    base_risk_profile_service_input.data.dependents = 3
    result = RiskProfileService.get_disability_risk_appetite(
        base_risk_profile_service_input, base_score=2
    )
    assert result.score == 3
    assert result.profile == InsuranceProfile.RESPONSIBLE
