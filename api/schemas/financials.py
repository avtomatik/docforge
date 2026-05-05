from pydantic import BaseModel


class PremiumAllocation(BaseModel):
    document_id: int
    underwriter_id: int

    net_amount: float
