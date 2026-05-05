from enum import Enum, StrEnum, auto

from core.config import settings
from core.constants import DATE


class Data(StrEnum):

    CERTIFICATE = "certificate"
    CONTACTS = "contacts"
    CONTRACT = "contract"
    COUNTRY = "country"
    DEBIT_NOTE = "debit_note"
    LETTER = "letter"
    SERVICES_ACT = "services_act"

    @property
    def table_name(self):
        return self.value


class Template(Enum):

    def _generate_next_value_(name, *args):
        return name

    ACT = auto()
    ADDENDUM = auto()
    COVER_NOTE = auto()
    DEBIT_NOTE = auto()
    ENDORSEMENT = auto()
    LETTER = auto()
    LETTER_0x9 = auto()
    LETTER_CEM = auto()
    LETTER_FIRM_ORDER = auto()
    LETTER_WARRANTY = auto()
    NDA = auto()
    SCOPES = auto()
    SERVICES_ACT = auto()
    SLIP = auto()
    SLIP_TREATY = auto()
    SPECIAL_ACCEPTANCE = auto()

    @property
    def template_name(self):

        if self.value == "SLIP_TREATY":
            return f"template_treaty_{settings.ACCOUNT_NAME}{DATE:%Y}_endorsement_{DATE}.docx"

        return f"{self.value.lower()}.docx"


class Currency(StrEnum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    RUB = "RUB"


class DocumentType(StrEnum):
    COVER_NOTE = "cover_note"
    DEBIT_NOTE = "debit_note"
    ENDORSEMENT = "endorsement"
    ADDENDUM = "addendum"
    LETTER = "letter"


class DocumentStatus(StrEnum):
    DRAFT = "draft"
    ISSUED = "issued"
    SENT = "sent"
    CANCELLED = "cancelled"


class PlacementStatus(StrEnum):
    OPEN = "open"
    PARTIALLY_PLACED = "partial"
    PLACED = "placed"
    BOUND = "bound"
    CANCELLED = "cancelled"


class PartyRoleType(StrEnum):
    BROKER = "broker"
    INSURED = "insured"
    REINSURED = "reinsured"
    UNDERWRITER = "underwriter"
