from sqlalchemy.orm import Session
from typing import List, Optional, Type, TypeVar, Generic
from app.models import models
from app.schemas import schemas

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType
    ) -> ModelType:
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj


# Hotel CRUD
class CRUDHotel(CRUDBase[models.Hotel, schemas.HotelCreate, schemas.HotelUpdate]):
    pass


# Activity CRUD
class CRUDActivity(CRUDBase[models.Activity, schemas.ActivityCreate, schemas.ActivityUpdate]):
    pass


# Transfer CRUD
class CRUDTransfer(CRUDBase[models.Transfer, schemas.TransferCreate, schemas.TransferUpdate]):
    pass


# Meal CRUD
class CRUDMeal(CRUDBase[models.Meal, schemas.MealCreate, schemas.MealUpdate]):
    pass


# Customer CRUD
class CRUDCustomer(CRUDBase[models.Customer, schemas.CustomerCreate, schemas.CustomerUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[models.Customer]:
        return db.query(models.Customer).filter(models.Customer.email == email).first()


# Enquiry CRUD
class CRUDEnquiry(CRUDBase[models.Enquiry, schemas.EnquiryCreate, schemas.EnquiryUpdate]):
    def get_by_customer(self, db: Session, *, customer_id: int) -> List[models.Enquiry]:
        return db.query(models.Enquiry).filter(models.Enquiry.customer_id == customer_id).all()


# Itinerary CRUD
class CRUDItinerary(CRUDBase[models.Itinerary, schemas.ItineraryCreate, schemas.ItineraryUpdate]):
    def create_with_items(
        self, db: Session, *, obj_in: schemas.ItineraryCreate
    ) -> models.Itinerary:
        obj_in_data = obj_in.model_dump(exclude={"items"})
        db_obj = models.Itinerary(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # Add items
        if obj_in.items:
            for item_data in obj_in.items:
                item_dict = item_data.model_dump()
                item_dict["itinerary_id"] = db_obj.id
                db_item = models.ItineraryItem(**item_dict)
                db.add(db_item)
            db.commit()
            db.refresh(db_obj)
        
        # Calculate total price
        self.calculate_total_price(db, itinerary_id=db_obj.id)
        
        return db_obj

    def calculate_total_price(self, db: Session, *, itinerary_id: int):
        itinerary = db.query(models.Itinerary).filter(models.Itinerary.id == itinerary_id).first()
        if not itinerary:
            return
        
        total = 0.0
        for item in itinerary.items:
            if item.hotel and item.hotel.pricing:
                total += item.hotel.pricing
            if item.activity and item.activity.pricing:
                total += item.activity.pricing
            if item.transfer and item.transfer.pricing:
                total += item.transfer.pricing
            if item.meal and item.meal.pricing:
                total += item.meal.pricing
        
        itinerary.total_price = total
        db.add(itinerary)
        db.commit()


# Itinerary Item CRUD
class CRUDItineraryItem(CRUDBase[models.ItineraryItem, schemas.ItineraryItemCreate, schemas.ItineraryItemUpdate]):
    def create_item(
        self, db: Session, *, itinerary_id: int, obj_in: schemas.ItineraryItemCreate
    ) -> models.ItineraryItem:
        obj_in_data = obj_in.model_dump()
        obj_in_data["itinerary_id"] = itinerary_id
        db_obj = models.ItineraryItem(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # Recalculate itinerary total
        crud_itinerary.calculate_total_price(db, itinerary_id=itinerary_id)
        
        return db_obj

    def get_by_itinerary(self, db: Session, *, itinerary_id: int) -> List[models.ItineraryItem]:
        return db.query(models.ItineraryItem).filter(
            models.ItineraryItem.itinerary_id == itinerary_id
        ).order_by(models.ItineraryItem.day_number, models.ItineraryItem.item_order).all()


# Quote CRUD
class CRUDQuote(CRUDBase[models.Quote, schemas.QuoteCreate, schemas.QuoteUpdate]):
    def create_quote(self, db: Session, *, obj_in: schemas.QuoteCreate) -> models.Quote:
        # Get itinerary to calculate base price
        itinerary = db.query(models.Itinerary).filter(
            models.Itinerary.id == obj_in.itinerary_id
        ).first()
        
        base_price = obj_in.base_price if obj_in.base_price else (itinerary.total_price if itinerary else 0.0)
        total_price = base_price * (1 + obj_in.markup_percentage / 100)
        
        obj_in_data = obj_in.model_dump()
        obj_in_data["base_price"] = base_price
        obj_in_data["total_price"] = total_price
        
        db_obj = models.Quote(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_enquiry(self, db: Session, *, enquiry_id: int) -> List[models.Quote]:
        return db.query(models.Quote).filter(models.Quote.enquiry_id == enquiry_id).all()


# Initialize CRUD instances
crud_hotel = CRUDHotel(models.Hotel)
crud_activity = CRUDActivity(models.Activity)
crud_transfer = CRUDTransfer(models.Transfer)
crud_meal = CRUDMeal(models.Meal)
crud_customer = CRUDCustomer(models.Customer)
crud_enquiry = CRUDEnquiry(models.Enquiry)
crud_itinerary = CRUDItinerary(models.Itinerary)
crud_itinerary_item = CRUDItineraryItem(models.ItineraryItem)
crud_quote = CRUDQuote(models.Quote)
