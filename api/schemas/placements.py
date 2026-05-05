from datetime import datetime

from pydantic import BaseModel

from core.enums import Currency, PlacementStatus


class Placement(BaseModel):
    id: int
    umr: str

    broker_id: int
    insured_id: int

    currency: Currency
    status: PlacementStatus

    inception_date: datetime
    expiry_date: datetime
