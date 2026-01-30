from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas import schemas
from app.crud import crud

router = APIRouter()


@router.post("/", response_model=schemas.Package)
def create_package(package: schemas.PackageCreate, db: Session = Depends(get_db)):
    """Create a new package with optional items"""
    return crud.crud_package.create_with_items(db=db, obj_in=package)


@router.get("/", response_model=List[schemas.Package])
def list_packages(
    skip: int = 0, 
    limit: int = 100, 
    active_only: bool = False,
    db: Session = Depends(get_db)
):
    """List all packages"""
    if active_only:
        return crud.crud_package.get_active_packages(db=db)
    return crud.crud_package.get_multi(db=db, skip=skip, limit=limit)


@router.get("/{package_id}", response_model=schemas.Package)
def get_package(package_id: int, db: Session = Depends(get_db)):
    """Get a specific package with all its items"""
    package = crud.crud_package.get(db=db, id=package_id)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    return package


@router.put("/{package_id}", response_model=schemas.Package)
def update_package(
    package_id: int, 
    package: schemas.PackageUpdate, 
    db: Session = Depends(get_db)
):
    """Update a package"""
    db_package = crud.crud_package.get(db=db, id=package_id)
    if not db_package:
        raise HTTPException(status_code=404, detail="Package not found")
    return crud.crud_package.update(db=db, db_obj=db_package, obj_in=package)


@router.delete("/{package_id}")
def delete_package(package_id: int, db: Session = Depends(get_db)):
    """Delete a package"""
    package = crud.crud_package.get(db=db, id=package_id)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    crud.crud_package.delete(db=db, id=package_id)
    return {"message": "Package deleted successfully"}


@router.post("/{package_id}/create-itinerary", response_model=schemas.Itinerary)
def create_itinerary_from_package(
    package_id: int,
    itinerary_name: str,
    selected_options: dict = None,
    db: Session = Depends(get_db)
):
    """
    Create an itinerary from a package template
    selected_options: dict of option_group -> selected_item_id for choosing from package options
    """
    package = crud.crud_package.get(db=db, id=package_id)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    
    # Create itinerary
    itinerary_data = schemas.ItineraryCreate(
        name=itinerary_name,
        description=f"Created from package: {package.name}",
        currency_id=package.currency_id,
        package_id=package.id,
        items=[]
    )
    
    # Process package items
    for package_item in package.package_items:
        # If item is optional and has an option_group
        if package_item.is_optional and package_item.option_group:
            # Check if this option was selected
            if selected_options and package_item.option_group in selected_options:
                selected_id = selected_options[package_item.option_group]
                # Only add if this specific item was selected
                if package_item.id == selected_id:
                    itinerary_item = schemas.ItineraryItemCreate(
                        day_number=package_item.day_number,
                        item_type=package_item.item_type,
                        item_order=package_item.item_order,
                        hotel_id=package_item.hotel_id,
                        activity_id=package_item.activity_id,
                        transfer_id=package_item.transfer_id,
                        meal_id=package_item.meal_id,
                        notes=package_item.notes
                    )
                    itinerary_data.items.append(itinerary_item)
        else:
            # Non-optional items are always included
            itinerary_item = schemas.ItineraryItemCreate(
                day_number=package_item.day_number,
                item_type=package_item.item_type,
                item_order=package_item.item_order,
                hotel_id=package_item.hotel_id,
                activity_id=package_item.activity_id,
                transfer_id=package_item.transfer_id,
                meal_id=package_item.meal_id,
                notes=package_item.notes
            )
            itinerary_data.items.append(itinerary_item)
    
    return crud.crud_itinerary.create_with_items(db=db, obj_in=itinerary_data)
