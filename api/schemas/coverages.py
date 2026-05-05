from pydantic import BaseModel


class CoverageSection(BaseModel):
    id: int
    code: str  # PD, BI, TPL
    name: str


class PlacementCoverage(BaseModel):
    placement_id: int
    coverage_section_id: int

    limit: float | None = None
    deductible: float | None = None
    rate: float | None = None
    pml: float | None = None
