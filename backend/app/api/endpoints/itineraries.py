from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas import schemas
from app.crud import crud

router = APIRouter()


@router.post("/", response_model=schemas.Itinerary)
def create_itinerary(itinerary: schemas.ItineraryCreate, db: Session = Depends(get_db)):
    """Create a new itinerary with items"""
    return crud.crud_itinerary.create_with_items(db=db, obj_in=itinerary)


@router.get("/", response_model=List[schemas.Itinerary])
def list_itineraries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all itineraries"""
    return crud.crud_itinerary.get_multi(db=db, skip=skip, limit=limit)


@router.get("/{itinerary_id}", response_model=schemas.Itinerary)
def get_itinerary(itinerary_id: int, db: Session = Depends(get_db)):
    """Get a specific itinerary"""
    itinerary = crud.crud_itinerary.get(db=db, id=itinerary_id)
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return itinerary


@router.put("/{itinerary_id}", response_model=schemas.Itinerary)
def update_itinerary(itinerary_id: int, itinerary: schemas.ItineraryUpdate, db: Session = Depends(get_db)):
    """Update an itinerary"""
    db_itinerary = crud.crud_itinerary.get(db=db, id=itinerary_id)
    if not db_itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return crud.crud_itinerary.update(db=db, db_obj=db_itinerary, obj_in=itinerary)


@router.delete("/{itinerary_id}")
def delete_itinerary(itinerary_id: int, db: Session = Depends(get_db)):
    """Delete an itinerary"""
    itinerary = crud.crud_itinerary.get(db=db, id=itinerary_id)
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    crud.crud_itinerary.delete(db=db, id=itinerary_id)
    return {"message": "Itinerary deleted successfully"}


# Itinerary Items endpoints
@router.post("/{itinerary_id}/items", response_model=schemas.ItineraryItem)
def add_itinerary_item(itinerary_id: int, item: schemas.ItineraryItemCreate, db: Session = Depends(get_db)):
    """Add an item to an itinerary"""
    itinerary = crud.crud_itinerary.get(db=db, id=itinerary_id)
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return crud.crud_itinerary_item.create_item(db=db, itinerary_id=itinerary_id, obj_in=item)


@router.get("/{itinerary_id}/items", response_model=List[schemas.ItineraryItem])
def get_itinerary_items(itinerary_id: int, db: Session = Depends(get_db)):
    """Get all items for an itinerary"""
    return crud.crud_itinerary_item.get_by_itinerary(db=db, itinerary_id=itinerary_id)


@router.put("/items/{item_id}", response_model=schemas.ItineraryItem)
def update_itinerary_item(item_id: int, item: schemas.ItineraryItemUpdate, db: Session = Depends(get_db)):
    """Update an itinerary item"""
    db_item = crud.crud_itinerary_item.get(db=db, id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Itinerary item not found")
    return crud.crud_itinerary_item.update(db=db, db_obj=db_item, obj_in=item)


@router.delete("/items/{item_id}")
def delete_itinerary_item(item_id: int, db: Session = Depends(get_db)):
    """Delete an itinerary item"""
    item = crud.crud_itinerary_item.get(db=db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Itinerary item not found")
    itinerary_id = item.itinerary_id
    crud.crud_itinerary_item.delete(db=db, id=item_id)
    # Recalculate total price
    crud.crud_itinerary.calculate_total_price(db=db, itinerary_id=itinerary_id)
    return {"message": "Itinerary item deleted successfully"}
