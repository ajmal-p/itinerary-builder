from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas import schemas
from app.crud import crud

router = APIRouter()


@router.post("/", response_model=schemas.Transfer)
def create_transfer(transfer: schemas.TransferCreate, db: Session = Depends(get_db)):
    """Create a new transfer"""
    return crud.crud_transfer.create(db=db, obj_in=transfer)


@router.get("/", response_model=List[schemas.Transfer])
def list_transfers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all transfers"""
    return crud.crud_transfer.get_multi(db=db, skip=skip, limit=limit)


@router.get("/{transfer_id}", response_model=schemas.Transfer)
def get_transfer(transfer_id: int, db: Session = Depends(get_db)):
    """Get a specific transfer"""
    transfer = crud.crud_transfer.get(db=db, id=transfer_id)
    if not transfer:
        raise HTTPException(status_code=404, detail="Transfer not found")
    return transfer


@router.put("/{transfer_id}", response_model=schemas.Transfer)
def update_transfer(transfer_id: int, transfer: schemas.TransferUpdate, db: Session = Depends(get_db)):
    """Update a transfer"""
    db_transfer = crud.crud_transfer.get(db=db, id=transfer_id)
    if not db_transfer:
        raise HTTPException(status_code=404, detail="Transfer not found")
    return crud.crud_transfer.update(db=db, db_obj=db_transfer, obj_in=transfer)


@router.delete("/{transfer_id}")
def delete_transfer(transfer_id: int, db: Session = Depends(get_db)):
    """Delete a transfer"""
    transfer = crud.crud_transfer.get(db=db, id=transfer_id)
    if not transfer:
        raise HTTPException(status_code=404, detail="Transfer not found")
    crud.crud_transfer.delete(db=db, id=transfer_id)
    return {"message": "Transfer deleted successfully"}
