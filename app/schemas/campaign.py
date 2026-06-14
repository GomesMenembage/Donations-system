from datetime import date, datetime

from pydantic import BaseModel


class CampaignCreate(BaseModel):
    title: str
    donation_type: str
    goal: str | None = None
    deadline: date | None = None


class CampaignOut(BaseModel):
    id: int
    center_id: int
    title: str
    donation_type: str
    goal: str | None = None
    deadline: date | None = None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
