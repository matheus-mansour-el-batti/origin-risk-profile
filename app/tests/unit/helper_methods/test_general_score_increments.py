from app.services.risk_profile import RiskProfileService


def test_score_increment_by_income__high_income():
    result = RiskProfileService.get_general_score_increment_by_income(income=300000)
    assert result == -1


def test_score_increment_by_income__normal_income():
    result = RiskProfileService.get_general_score_increment_by_income(income=100000)
    assert result == 0


def test_score_increment_by_age__very_low_age():
    result = RiskProfileService.get_general_score_increment_by_age(age=19)
    assert result == -2


def test_score_increment_by_age___low_age():
    result = RiskProfileService.get_general_score_increment_by_age(age=35)
    assert result == -1


def test_score_increment_by_age___normal_age():
    result = RiskProfileService.get_general_score_increment_by_age(age=50)
    assert result == 0
