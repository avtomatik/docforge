from datetime import datetime

from pydantic import BaseModel


class Order(BaseModel):
    id: int
    placement_id: int

    target_percentage: float
    effective_date: datetime
