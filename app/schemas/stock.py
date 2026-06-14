from datetime import datetime

from pydantic import BaseModel


class StockOut(BaseModel):
    id: int
    center_id: int
    donation_type: str
    quantity: str
    updated_at: datetime

    model_config = {"from_attributes": True}
