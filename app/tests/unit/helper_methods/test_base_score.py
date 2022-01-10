from app.services.risk_profile import RiskProfileService


def test_get_base_score():
    result = RiskProfileService.get_base_score(risk_questions=[True, True, True])
    assert result == 3
    result = RiskProfileService.get_base_score(risk_questions=[True, False, True])
    assert result == 2
    result = RiskProfileService.get_base_score(risk_questions=[False, False, True])
    assert result == 1
    result = RiskProfileService.get_base_score(risk_questions=[False, False, False])
    assert result == 0
