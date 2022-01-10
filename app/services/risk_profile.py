import datetime
from typing import List

from app.config.settings import (
    LOWER_BOUND_SCORE_FOR_REGULAR_PROFILE,
    LOWER_BOUND_SCORE_FOR_RESPONSIBLE_PROFILE,
    MAX_AGE_FOR_DISABILITY_AND_LIFE_ELIGIBILITY,
    MAX_AGE_FOR_HIGH_RISK_APPETITE,
    MAX_AGE_FOR_VERY_HIGH_RISK_APPETITE,
    MAX_VEHICLE_PRODUCTION_AGE_FOR_LOW_RISK_APPETITE,
    MIN_AGE_FOR_HIGH_RISK_APPETITE,
    MIN_INCOME_FOR_HIGH_RISK_APPETITE,
)
from app.schemas.request.risk_profile import MaritalStatus, OwnershipStatus
from app.schemas.response.risk_profile import InsuranceRecommendation
from app.schemas.risk_profile import (
    InsuranceProfile,
    InsuranceProfileDivision,
    RiskAppetite,
)


class RiskProfileService:
    """
    This Class allows the calculation of the risk profile recommendation for each insurance line.
    """

    def __init__(self, data):
        self.data = data
        self.divisions = [
            InsuranceProfileDivision(
                lower_bound=LOWER_BOUND_SCORE_FOR_RESPONSIBLE_PROFILE,
                profile=InsuranceProfile.RESPONSIBLE,
            ),
            InsuranceProfileDivision(
                lower_bound=LOWER_BOUND_SCORE_FOR_REGULAR_PROFILE,
                profile=InsuranceProfile.REGULAR,
            ),
        ]

    def get_risk_profile(self) -> InsuranceRecommendation:

        """
        Main function. Uses RiskProfileService data to return
        InsuranceRecommendation Schema with recommended profile for each insurance line
        """
        base_score = self.get_base_score(risk_questions=self.data.risk_questions)

        auto_risk_appetite = self.get_auto_risk_appetite(base_score=base_score)
        disability_risk_appetite = self.get_disability_risk_appetite(
            base_score=base_score
        )
        home_risk_appetite = self.get_home_risk_appetite(base_score=base_score)
        life_risk_appetite = self.get_life_risk_appetite(base_score=base_score)

        return InsuranceRecommendation(
            auto=auto_risk_appetite.profile,
            disability=disability_risk_appetite.profile,
            home=home_risk_appetite.profile,
            life=life_risk_appetite.profile,
        )

    def get_auto_risk_appetite(self, base_score: int) -> RiskAppetite:
        """
        Uses "base_score" to return RiskAppetite schema with score and risk profile for auto insurance line.
        """
        if not self.data.vehicle:
            return RiskAppetite(profile=InsuranceProfile.INELIGIBLE)

        auto_risk_score = base_score
        auto_risk_score += self.get_general_score_increment_by_age(age=self.data.age)
        auto_risk_score += self.get_general_score_increment_by_income(
            income=self.data.income
        )
        auto_risk_score += self.get_auto_score_increment_by_production_year(
            production_year=self.data.vehicle.year
        )

        return RiskAppetite(
            score=auto_risk_score,
            profile=self.get_risk_profile_from_score(risk_score=auto_risk_score),
        )

    def get_disability_risk_appetite(self, base_score: int) -> RiskAppetite:
        """
        Uses "base_score" to return RiskAppetite schema with score and risk profile for disability insurance line.
        """

        if (
            self.data.income == 0
            or self.data.age > MAX_AGE_FOR_DISABILITY_AND_LIFE_ELIGIBILITY
        ):
            return RiskAppetite(profile=InsuranceProfile.INELIGIBLE)

        disability_risk_score = base_score
        disability_risk_score += self.get_general_score_increment_by_age(
            age=self.data.age
        )
        disability_risk_score += self.get_general_score_increment_by_income(
            income=self.data.income
        )
        if self.data.house == OwnershipStatus.MORTGAGED:
            disability_risk_score += 1
        if self.data.dependents > 0:
            disability_risk_score += 1
        if self.data.marital_status == MaritalStatus.MARRIED:
            disability_risk_score -= 1

        return RiskAppetite(
            score=disability_risk_score,
            profile=self.get_risk_profile_from_score(risk_score=disability_risk_score),
        )

    def get_home_risk_appetite(self, base_score: int) -> RiskAppetite:
        """
        Uses "base_score" to return RiskAppetite schema with score and risk profile for home insurance line.
        """

        if not self.data.house:
            return RiskAppetite(profile=InsuranceProfile.INELIGIBLE)

        home_risk_score = base_score
        home_risk_score += self.get_general_score_increment_by_age(age=self.data.age)
        home_risk_score += self.get_general_score_increment_by_income(
            income=self.data.income
        )
        if self.data.house == OwnershipStatus.MORTGAGED:
            home_risk_score += 1

        return RiskAppetite(
            score=home_risk_score,
            profile=self.get_risk_profile_from_score(risk_score=home_risk_score),
        )

    def get_life_risk_appetite(self, base_score: int) -> RiskAppetite:
        """
        Uses "base_score" to return RiskAppetite schema with score and risk profile for life insurance line.
        """

        if self.data.age > MAX_AGE_FOR_DISABILITY_AND_LIFE_ELIGIBILITY:
            return RiskAppetite(profile=InsuranceProfile.INELIGIBLE)

        life_risk_score = base_score
        life_risk_score += self.get_general_score_increment_by_age(age=self.data.age)
        life_risk_score += self.get_general_score_increment_by_income(
            income=self.data.income
        )
        if self.data.dependents > 0:
            life_risk_score += 1
        if self.data.marital_status == MaritalStatus.MARRIED:
            life_risk_score += 1

        return RiskAppetite(
            score=life_risk_score,
            profile=self.get_risk_profile_from_score(risk_score=life_risk_score),
        )

    def get_risk_profile_from_score(self, risk_score: int) -> InsuranceProfile:

        """
        Maps "risk_score" to a specific InsuranceProfile appetite category according
        to the divisions business rule.
        """

        for candidate_division in self.divisions:
            if risk_score >= candidate_division.lower_bound:
                return candidate_division.profile
        return InsuranceProfile.ECONOMIC

    @staticmethod
    def get_base_score(risk_questions: List[bool]) -> int:
        """
        Returns the base score according to the boolean risk_questions asked.
        """
        return sum(risk_questions)

    @staticmethod
    def get_general_score_increment_by_age(age: int) -> int:
        """
        Returns the given general score increments according to payload´s age.
        """
        if age < MAX_AGE_FOR_VERY_HIGH_RISK_APPETITE:
            return -2
        if (
            age >= MIN_AGE_FOR_HIGH_RISK_APPETITE
            and age <= MAX_AGE_FOR_HIGH_RISK_APPETITE
        ):
            return -1
        return 0

    @staticmethod
    def get_general_score_increment_by_income(income: int) -> int:
        """
        Returns the given general score increments according to payload´s income.
        """
        if income > MIN_INCOME_FOR_HIGH_RISK_APPETITE:
            return -1
        return 0

    @staticmethod
    def get_auto_score_increment_by_production_year(production_year: int) -> int:
        """
        Returns the specific score increments according to the vehicle´s production year.
        """
        current_date = datetime.date.today()
        current_year = int(current_date.strftime("%Y"))
        if (
            production_year
            >= current_year - MAX_VEHICLE_PRODUCTION_AGE_FOR_LOW_RISK_APPETITE
        ):
            return 1
        return 0
