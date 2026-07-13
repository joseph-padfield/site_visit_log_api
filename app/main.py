from datetime import date

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Query,
    status
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas
from .database import get_db

app = FastAPI(
    title="Site Visit Log API",
    description=("A small API for recording heritage sites" \
    "and inspection visits."),
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {
        "message": "Site Visit Log API is running."
    }

@app.post(
        "/sites/",
        response_model=schemas.SiteResponse,
        status_code=status.HTTP_201_CREATED
        )
def create_site(
    site_data: schemas.SiteCreate,
    db: Session = Depends(get_db)
):
    site = models.Site(
        name=site_data.name,
        address=site_data.address,
        site_type=site_data.site_type,
        notes=site_data.notes
    )

    db.add(site)
    db.commit()
    db.refresh(site)

    return site


@app.get(
    "/sites/",
    response_model=list[schemas.SiteResponse]
)
def read_sites(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    statement = (
        select(models.Site)
        .order_by(models.Site.name)
        .offset(skip)
        .limit(limit)
    )

    return db.scalars(statement).all()


@app.get(
    "/sites/{site_id}",
    response_model=schemas.SiteResponse
)
def read_site(
    site_id: int,
    db: Session = Depends(get_db)
):
    site = db.get(models.Site, site_id)

    if site is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found."
        )
    
    return site

@app.post(
    "/sites/{site_id}/visits/",
    response_model=schemas.VisitResponse,
    status_code=status.HTTP_201_CREATED
)
def create_visit(
    site_id: int,
    visit_data: schemas.VisitCreate,
    db: Session = Depends(get_db)
):
    site = db.get(models.Site, site_id)

    if site is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found."
        )
    
    visit = models.Visit(
        site_id=site_id,
        visit_date=visit_data.visit_date,
        purpose=visit_data.purpose,
        weather=visit_data.weather,
        notes=visit_data.notes
    )

    db.add(visit)
    db.commit()
    db.refresh(visit)

    return visit


@app.get(
    "/sites/{site_id}/visits/",
    response_model=list[schemas.VisitResponse]
)
def read_site_visits(
    site_id: int,
    db: Session = Depends(get_db)
):
    site = db.get(models.Site, site_id)

    if site is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found."
        )
    
    statement = (
        select(models.Visit)
        .where(models.Visit.site_id == site_id)
        .order_by(models.Visit.visit_date.desc())
    )

    return db.scalars(statement).all()