from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas import schemas
from app.crud import crud

router = APIRouter()


@router.post("/", response_model=schemas.Activity)
def create_activity(activity: schemas.ActivityCreate, db: Session = Depends(get_db)):
    """Create a new activity"""
    return crud.crud_activity.create(db=db, obj_in=activity)


@router.get("/", response_model=List[schemas.Activity])
def list_activities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all activities"""
    return crud.crud_activity.get_multi(db=db, skip=skip, limit=limit)


@router.get("/{activity_id}", response_model=schemas.Activity)
def get_activity(activity_id: int, db: Session = Depends(get_db)):
    """Get a specific activity"""
    activity = crud.crud_activity.get(db=db, id=activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.put("/{activity_id}", response_model=schemas.Activity)
def update_activity(activity_id: int, activity: schemas.ActivityUpdate, db: Session = Depends(get_db)):
    """Update an activity"""
    db_activity = crud.crud_activity.get(db=db, id=activity_id)
    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return crud.crud_activity.update(db=db, db_obj=db_activity, obj_in=activity)


@router.delete("/{activity_id}")
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    """Delete an activity"""
    activity = crud.crud_activity.get(db=db, id=activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    crud.crud_activity.delete(db=db, id=activity_id)
    return {"message": "Activity deleted successfully"}
