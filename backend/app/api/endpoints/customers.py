from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas import schemas
from app.crud import crud

router = APIRouter()


@router.post("/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    """Create a new customer"""
    # Check if email already exists
    existing = crud.crud_customer.get_by_email(db=db, email=customer.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.crud_customer.create(db=db, obj_in=customer)


@router.get("/", response_model=List[schemas.Customer])
def list_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all customers"""
    return crud.crud_customer.get_multi(db=db, skip=skip, limit=limit)


@router.get("/{customer_id}", response_model=schemas.Customer)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """Get a specific customer"""
    customer = crud.crud_customer.get(db=db, id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.put("/{customer_id}", response_model=schemas.Customer)
def update_customer(customer_id: int, customer: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    """Update a customer"""
    db_customer = crud.crud_customer.get(db=db, id=customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return crud.crud_customer.update(db=db, db_obj=db_customer, obj_in=customer)


@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """Delete a customer"""
    customer = crud.crud_customer.get(db=db, id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    crud.crud_customer.delete(db=db, id=customer_id)
    return {"message": "Customer deleted successfully"}
