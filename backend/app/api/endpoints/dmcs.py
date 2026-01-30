from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas import schemas
from app.crud import crud

router = APIRouter()


@router.post("/", response_model=schemas.DMC)
def create_dmc(dmc: schemas.DMCCreate, db: Session = Depends(get_db)):
    """Create a new DMC (Destination Management Company)"""
    return crud.crud_dmc.create(db=db, obj_in=dmc)


@router.get("/", response_model=List[schemas.DMC])
def list_dmcs(
    skip: int = 0, 
    limit: int = 100, 
    active_only: bool = False,
    destination: str = None,
    db: Session = Depends(get_db)
):
    """List all DMCs"""
    if destination:
        return crud.crud_dmc.get_by_destination(db=db, destination=destination)
    if active_only:
        return crud.crud_dmc.get_active_dmcs(db=db)
    return crud.crud_dmc.get_multi(db=db, skip=skip, limit=limit)


@router.get("/{dmc_id}", response_model=schemas.DMC)
def get_dmc(dmc_id: int, db: Session = Depends(get_db)):
    """Get a specific DMC"""
    dmc = crud.crud_dmc.get(db=db, id=dmc_id)
    if not dmc:
        raise HTTPException(status_code=404, detail="DMC not found")
    return dmc


@router.put("/{dmc_id}", response_model=schemas.DMC)
def update_dmc(dmc_id: int, dmc: schemas.DMCUpdate, db: Session = Depends(get_db)):
    """Update a DMC"""
    db_dmc = crud.crud_dmc.get(db=db, id=dmc_id)
    if not db_dmc:
        raise HTTPException(status_code=404, detail="DMC not found")
    return crud.crud_dmc.update(db=db, db_obj=db_dmc, obj_in=dmc)


@router.delete("/{dmc_id}")
def delete_dmc(dmc_id: int, db: Session = Depends(get_db)):
    """Delete a DMC"""
    dmc = crud.crud_dmc.get(db=db, id=dmc_id)
    if not dmc:
        raise HTTPException(status_code=404, detail="DMC not found")
    crud.crud_dmc.delete(db=db, id=dmc_id)
    return {"message": "DMC deleted successfully"}
