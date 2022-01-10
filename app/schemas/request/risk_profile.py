from enum import Enum
from typing import Optional

from pydantic import BaseModel
from pydantic.types import NonNegativeInt, conlist


class MaritalStatus(Enum):
    MARRIED = "married"
    SINGLE = "single"


class OwnershipStatus(Enum):
    OWNED = "owned"
    MORTGAGED = "mortgaged"


class House(BaseModel):
    ownership_status: OwnershipStatus


class Vehicle(BaseModel):
    year: NonNegativeInt


class UserAttributes(BaseModel):
    age: NonNegativeInt
    dependents: NonNegativeInt
    income: NonNegativeInt
    marital_status: MaritalStatus
    risk_questions: conlist(item_type=bool, min_items=3, max_items=3)


class RiskProfileInput(UserAttributes):
    house: Optional[House]
    vehicle: Optional[Vehicle]
