from pydantic import BaseModel

from api.schemas.coverages import PlacementCoverage
from api.schemas.documents import Document
from api.schemas.lines import LineWritten
from api.schemas.orders import Order
from api.schemas.parties import PartyRole
from api.schemas.placements import Placement
from api.schemas.structures import Layer


class PlacementAggregate(BaseModel):
    placement: Placement

    parties: list[PartyRole]
    documents: list[Document]

    orders: list[Order]

    lines: list[LineWritten]
    coverages: list[PlacementCoverage]
    layers: list[Layer]

    current_effective_document: Document | None = None
