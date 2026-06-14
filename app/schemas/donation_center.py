from datetime import datetime

from pydantic import BaseModel


class DonationCenterCreate(BaseModel):
    name: str
    address: str
    phone: str
    schedule: str | None = None


class DonationCenterUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    phone: str | None = None
    schedule: str | None = None


class DonationCenterOut(BaseModel):
    id: int
    user_id: int
    name: str
    address: str
    phone: str
    schedule: str | None = None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
