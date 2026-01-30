from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas import schemas
from app.crud import crud

router = APIRouter()


@router.post("/", response_model=schemas.Meal)
def create_meal(meal: schemas.MealCreate, db: Session = Depends(get_db)):
    """Create a new meal"""
    return crud.crud_meal.create(db=db, obj_in=meal)


@router.get("/", response_model=List[schemas.Meal])
def list_meals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all meals"""
    return crud.crud_meal.get_multi(db=db, skip=skip, limit=limit)


@router.get("/{meal_id}", response_model=schemas.Meal)
def get_meal(meal_id: int, db: Session = Depends(get_db)):
    """Get a specific meal"""
    meal = crud.crud_meal.get(db=db, id=meal_id)
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    return meal


@router.put("/{meal_id}", response_model=schemas.Meal)
def update_meal(meal_id: int, meal: schemas.MealUpdate, db: Session = Depends(get_db)):
    """Update a meal"""
    db_meal = crud.crud_meal.get(db=db, id=meal_id)
    if not db_meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    return crud.crud_meal.update(db=db, db_obj=db_meal, obj_in=meal)


@router.delete("/{meal_id}")
def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    """Delete a meal"""
    meal = crud.crud_meal.get(db=db, id=meal_id)
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    crud.crud_meal.delete(db=db, id=meal_id)
    return {"message": "Meal deleted successfully"}
