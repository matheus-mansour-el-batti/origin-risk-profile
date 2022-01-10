import datetime

from app.services.risk_profile import RiskProfileService


def test_auto_score_increment_by_production_year__recent_year():
    current_date = datetime.date.today()
    production_year = int(current_date.strftime("%Y")) - 2
    result = RiskProfileService.get_auto_score_increment_by_production_year(
        production_year=production_year
    )
    assert result == 1


def test_auto_score_increment_by_production_year__old_year():
    current_date = datetime.date.today()
    production_year = int(current_date.strftime("%Y")) - 7
    result = RiskProfileService.get_auto_score_increment_by_production_year(
        production_year=production_year
    )
    assert result == 0
