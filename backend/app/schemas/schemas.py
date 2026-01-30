from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# Enums
class EnquiryStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    CONVERTED = "converted"
    CLOSED = "closed"


class QuoteStatus(str, Enum):
    DRAFT = "draft"
    SENT = "sent"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class ItemType(str, Enum):
    HOTEL = "hotel"
    ACTIVITY = "activity"
    TRANSFER = "transfer"
    MEAL = "meal"


# Hotel Schemas
class HotelBase(BaseModel):
    name: str
    location: str
    star_rating: Optional[int] = None
    amenities: Optional[List[str]] = []
    pricing: Optional[float] = None
    images: Optional[List[str]] = []
    room_types: Optional[Dict[str, Any]] = {}
    description: Optional[str] = None


class HotelCreate(HotelBase):
    pass


class HotelUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    star_rating: Optional[int] = None
    amenities: Optional[List[str]] = None
    pricing: Optional[float] = None
    images: Optional[List[str]] = None
    room_types: Optional[Dict[str, Any]] = None
    description: Optional[str] = None


class Hotel(HotelBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Activity Schemas
class ActivityBase(BaseModel):
    name: str
    description: Optional[str] = None
    duration: Optional[str] = None
    location: Optional[str] = None
    pricing: Optional[float] = None
    category: Optional[str] = None
    time_slots: Optional[List[str]] = []
    images: Optional[List[str]] = []


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[str] = None
    location: Optional[str] = None
    pricing: Optional[float] = None
    category: Optional[str] = None
    time_slots: Optional[List[str]] = None
    images: Optional[List[str]] = None


class Activity(ActivityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Transfer Schemas
class TransferBase(BaseModel):
    transfer_type: str
    vehicle_type: Optional[str] = None
    capacity: Optional[int] = None
    pricing: Optional[float] = None
    pickup_point: Optional[str] = None
    dropoff_point: Optional[str] = None
    description: Optional[str] = None


class TransferCreate(TransferBase):
    pass


class TransferUpdate(BaseModel):
    transfer_type: Optional[str] = None
    vehicle_type: Optional[str] = None
    capacity: Optional[int] = None
    pricing: Optional[float] = None
    pickup_point: Optional[str] = None
    dropoff_point: Optional[str] = None
    description: Optional[str] = None


class Transfer(TransferBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Meal Schemas
class MealBase(BaseModel):
    meal_type: str
    cuisine: Optional[str] = None
    dietary_options: Optional[List[str]] = []
    pricing: Optional[float] = None
    venue: Optional[str] = None
    description: Optional[str] = None


class MealCreate(MealBase):
    pass


class MealUpdate(BaseModel):
    meal_type: Optional[str] = None
    cuisine: Optional[str] = None
    dietary_options: Optional[List[str]] = None
    pricing: Optional[float] = None
    venue: Optional[str] = None
    description: Optional[str] = None


class Meal(MealBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Customer Schemas
class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = {}


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None


class Customer(CustomerBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Enquiry Schemas
class EnquiryBase(BaseModel):
    customer_id: int
    status: EnquiryStatus = EnquiryStatus.NEW
    notes: Optional[str] = None


class EnquiryCreate(EnquiryBase):
    pass


class EnquiryUpdate(BaseModel):
    status: Optional[EnquiryStatus] = None
    notes: Optional[str] = None


class Enquiry(EnquiryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Itinerary Item Schemas
class ItineraryItemBase(BaseModel):
    day_number: int
    item_type: ItemType
    item_order: int = 0
    hotel_id: Optional[int] = None
    activity_id: Optional[int] = None
    transfer_id: Optional[int] = None
    meal_id: Optional[int] = None
    notes: Optional[str] = None


class ItineraryItemCreate(ItineraryItemBase):
    pass


class ItineraryItemUpdate(BaseModel):
    day_number: Optional[int] = None
    item_order: Optional[int] = None
    notes: Optional[str] = None


class ItineraryItem(ItineraryItemBase):
    id: int
    itinerary_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Itinerary Schemas
class ItineraryBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ItineraryCreate(ItineraryBase):
    items: Optional[List[ItineraryItemCreate]] = []


class ItineraryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class Itinerary(ItineraryBase):
    id: int
    total_price: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[ItineraryItem] = []
    
    class Config:
        from_attributes = True


# Quote Schemas
class QuoteBase(BaseModel):
    enquiry_id: int
    itinerary_id: int
    status: QuoteStatus = QuoteStatus.DRAFT
    base_price: Optional[float] = None
    markup_percentage: float = 0.0
    pricing_breakdown: Optional[Dict[str, Any]] = {}
    notes: Optional[str] = None


class QuoteCreate(QuoteBase):
    pass


class QuoteUpdate(BaseModel):
    status: Optional[QuoteStatus] = None
    markup_percentage: Optional[float] = None
    notes: Optional[str] = None


class Quote(QuoteBase):
    id: int
    total_price: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
