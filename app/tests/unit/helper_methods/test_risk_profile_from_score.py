from app.schemas.risk_profile import InsuranceProfile
from app.services.risk_profile import RiskProfileService


def test_risk_profile_from_score__negative_score(base_risk_profile_service_input):
    result = RiskProfileService.get_risk_profile_from_score(
        base_risk_profile_service_input, risk_score=-1
    )
    assert result == InsuranceProfile.ECONOMIC


def test_risk_profile_from_score__zero_score(base_risk_profile_service_input):
    result = RiskProfileService.get_risk_profile_from_score(
        base_risk_profile_service_input, risk_score=0
    )
    assert result == InsuranceProfile.ECONOMIC


def test_risk_profile_from_score__one_score(base_risk_profile_service_input):
    result = RiskProfileService.get_risk_profile_from_score(
        base_risk_profile_service_input, risk_score=1
    )
    assert result == InsuranceProfile.REGULAR


def test_risk_profile_from_score__two_score(base_risk_profile_service_input):
    result = RiskProfileService.get_risk_profile_from_score(
        base_risk_profile_service_input, risk_score=2
    )
    assert result == InsuranceProfile.REGULAR


def test_risk_profile_from_score__three_score(base_risk_profile_service_input):
    result = RiskProfileService.get_risk_profile_from_score(
        base_risk_profile_service_input, risk_score=3
    )
    assert result == InsuranceProfile.RESPONSIBLE


def test_risk_profile_from_score__four_score(base_risk_profile_service_input):
    result = RiskProfileService.get_risk_profile_from_score(
        base_risk_profile_service_input, risk_score=4
    )
    assert result == InsuranceProfile.RESPONSIBLE
