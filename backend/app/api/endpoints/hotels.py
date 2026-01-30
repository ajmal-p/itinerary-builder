from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas import schemas
from app.crud import crud

router = APIRouter()


@router.post("/", response_model=schemas.Hotel)
def create_hotel(hotel: schemas.HotelCreate, db: Session = Depends(get_db)):
    """Create a new hotel"""
    return crud.crud_hotel.create(db=db, obj_in=hotel)


@router.get("/", response_model=List[schemas.Hotel])
def list_hotels(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all hotels"""
    return crud.crud_hotel.get_multi(db=db, skip=skip, limit=limit)


@router.get("/{hotel_id}", response_model=schemas.Hotel)
def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    """Get a specific hotel"""
    hotel = crud.crud_hotel.get(db=db, id=hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel


@router.put("/{hotel_id}", response_model=schemas.Hotel)
def update_hotel(hotel_id: int, hotel: schemas.HotelUpdate, db: Session = Depends(get_db)):
    """Update a hotel"""
    db_hotel = crud.crud_hotel.get(db=db, id=hotel_id)
    if not db_hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return crud.crud_hotel.update(db=db, db_obj=db_hotel, obj_in=hotel)


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    """Delete a hotel"""
    hotel = crud.crud_hotel.get(db=db, id=hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    crud.crud_hotel.delete(db=db, id=hotel_id)
    return {"message": "Hotel deleted successfully"}
