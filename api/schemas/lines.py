from pydantic import BaseModel


class LineWritten(BaseModel):
    placement_id: int
    underwriter_id: int

    written_percentage: float
    signed_percentage: float

    layer_id: int | None = None
    document_id: int | None = None
