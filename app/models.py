from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    String,
    Text,
    false,
    func
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base

class Site(Base):
    __tablename__ = "sites"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    address: Mapped[str] = mapped_column(
        String(300),
        nullable=False
    )

    site_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    visits: Mapped[list[Visit]] = relationship(
        back_populates="site",
        passive_deletes=True
    )


class Visit(Base):
    __tablename__ = "visits"

    id: Mapped[int] = mapped_column(primary_key=True)

    site_id: Mapped[int] = mapped_column(
        ForeignKey(
            "sites.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    visit_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True
    )

    purpose: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    weather: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    site: Mapped[Site] = relationship(
        back_populates="visits"
    )

    follow_up_required: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=false()
    )