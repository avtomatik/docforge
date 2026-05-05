from pydantic import BaseModel

from core.enums import PartyRoleType


class Party(BaseModel):
    id: int

    name_en: str
    name_local: str | None = None

    address_en: str | None = None
    address_local: str | None = None

    country: str | None = None


class PartyRole(BaseModel):
    placement_id: int
    party_id: int
    role: PartyRoleType
