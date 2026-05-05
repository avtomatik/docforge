from datetime import datetime

from pydantic import BaseModel

from core.enums import DocumentStatus, DocumentType


class Document(BaseModel):
    id: int
    placement_id: int

    type: DocumentType
    status: DocumentStatus

    document_date: datetime
    effective_date: datetime | None = None

    document_number: int | str | None = None
