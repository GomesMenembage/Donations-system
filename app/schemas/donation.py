from datetime import date, datetime

from pydantic import BaseModel


class DonationRegister(BaseModel):
    center_id: int
    campaign_id: int | None = None
    type: str
    quantity: str
    date: date


class DonationOut(BaseModel):
    id: int
    donor_id: int
    center_id: int
    campaign_id: int | None = None
    type: str
    quantity: str
    date: date
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
