from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas import schemas
from app.crud import crud

router = APIRouter()


@router.post("/", response_model=schemas.Enquiry)
def create_enquiry(enquiry: schemas.EnquiryCreate, db: Session = Depends(get_db)):
    """Create a new enquiry"""
    # Verify customer exists
    customer = crud.crud_customer.get(db=db, id=enquiry.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return crud.crud_enquiry.create(db=db, obj_in=enquiry)


@router.get("/", response_model=List[schemas.Enquiry])
def list_enquiries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all enquiries"""
    return crud.crud_enquiry.get_multi(db=db, skip=skip, limit=limit)


@router.get("/{enquiry_id}", response_model=schemas.Enquiry)
def get_enquiry(enquiry_id: int, db: Session = Depends(get_db)):
    """Get a specific enquiry"""
    enquiry = crud.crud_enquiry.get(db=db, id=enquiry_id)
    if not enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")
    return enquiry


@router.get("/customer/{customer_id}", response_model=List[schemas.Enquiry])
def get_customer_enquiries(customer_id: int, db: Session = Depends(get_db)):
    """Get all enquiries for a customer"""
    return crud.crud_enquiry.get_by_customer(db=db, customer_id=customer_id)


@router.put("/{enquiry_id}", response_model=schemas.Enquiry)
def update_enquiry(enquiry_id: int, enquiry: schemas.EnquiryUpdate, db: Session = Depends(get_db)):
    """Update an enquiry"""
    db_enquiry = crud.crud_enquiry.get(db=db, id=enquiry_id)
    if not db_enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")
    return crud.crud_enquiry.update(db=db, db_obj=db_enquiry, obj_in=enquiry)


@router.delete("/{enquiry_id}")
def delete_enquiry(enquiry_id: int, db: Session = Depends(get_db)):
    """Delete an enquiry"""
    enquiry = crud.crud_enquiry.get(db=db, id=enquiry_id)
    if not enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")
    crud.crud_enquiry.delete(db=db, id=enquiry_id)
    return {"message": "Enquiry deleted successfully"}
