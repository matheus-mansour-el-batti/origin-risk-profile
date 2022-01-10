from pydantic import BaseModel

from app.schemas.risk_profile import InsuranceProfile


class InsuranceRecommendation(BaseModel):
    auto: InsuranceProfile
    disability: InsuranceProfile
    home: InsuranceProfile
    life: InsuranceProfile
