from enum import Enum
from typing import Optional

from pydantic import BaseModel


class InsuranceProfile(Enum):
    ECONOMIC = "economic"
    INELIGIBLE = "ineligible"
    REGULAR = "regular"
    RESPONSIBLE = "responsible"


class InsuranceProfileDivision(BaseModel):
    lower_bound: int
    profile: InsuranceProfile


class RiskAppetite(BaseModel):
    score: Optional[int] = None
    profile: InsuranceProfile
