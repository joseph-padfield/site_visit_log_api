from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class SiteCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=200
    )

    address: str = Field(
        min_length=1,
        max_length=300
    )

    site_type: str = Field(
        min_length=1,
        max_length=100
    )

    notes: str | None = None


class SiteResponse(BaseModel):
    id: int
    name: str
    address: str
    site_type: str
    notes: str | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class VisitCreate(BaseModel):
    visit_date: date

    purpose: str = Field(
        min_length=1,
        max_length=200
    )

    weather: str = Field(
        default=None,
        max_length=100
    )

    notes: str | None = None


class VisitResponse(BaseModel):
    id: int
    site_id: int
    visit_date: date
    purpose: str
    weather: str | None
    notes: str | None

    model_config = ConfigDict(
        from_attributes=True
    )
