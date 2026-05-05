from pydantic import BaseModel


class Layer(BaseModel):
    id: int
    placement_id: int

    attachment: float
    limit: float
