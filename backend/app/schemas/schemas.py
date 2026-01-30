from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from decimal import Decimal


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


# Currency Schemas
class CurrencyBase(BaseModel):
    code: str = Field(..., max_length=3, description="ISO 4217 currency code")
    name: str
    symbol: Optional[str] = None
    is_base_currency: bool = False
    is_active: bool = True


class CurrencyCreate(CurrencyBase):
    pass


class CurrencyUpdate(BaseModel):
    name: Optional[str] = None
    symbol: Optional[str] = None
    is_base_currency: Optional[bool] = None
    is_active: Optional[bool] = None


class Currency(CurrencyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Exchange Rate Schemas
class ExchangeRateBase(BaseModel):
    from_currency_id: int
    to_currency_id: int
    rate: Decimal = Field(..., description="Exchange rate with high precision")
    effective_date: datetime
    source: Optional[str] = None


class ExchangeRateCreate(ExchangeRateBase):
    pass


class ExchangeRateUpdate(BaseModel):
    rate: Optional[Decimal] = None
    effective_date: Optional[datetime] = None
    source: Optional[str] = None


class ExchangeRate(ExchangeRateBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# DMC Schemas
class DMCBase(BaseModel):
    company_name: str
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    destination: Optional[str] = None
    commission_percentage: float = 0.0
    payment_terms: Optional[str] = None
    notes: Optional[str] = None
    is_active: bool = True


class DMCCreate(DMCBase):
    pass


class DMCUpdate(BaseModel):
    company_name: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    destination: Optional[str] = None
    commission_percentage: Optional[float] = None
    payment_terms: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class DMC(DMCBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Package Item Schema
class PackageItemBase(BaseModel):
    day_number: int
    item_type: ItemType
    item_order: int = 0
    is_optional: bool = False
    option_group: Optional[str] = None
    hotel_id: Optional[int] = None
    activity_id: Optional[int] = None
    transfer_id: Optional[int] = None
    meal_id: Optional[int] = None
    notes: Optional[str] = None


class PackageItemCreate(PackageItemBase):
    pass


class PackageItemUpdate(BaseModel):
    day_number: Optional[int] = None
    item_order: Optional[int] = None
    is_optional: Optional[bool] = None
    option_group: Optional[str] = None
    notes: Optional[str] = None


class PackageItem(PackageItemBase):
    id: int
    package_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Package Schemas
class PackageBase(BaseModel):
    name: str
    description: Optional[str] = None
    destination: Optional[str] = None
    duration_days: Optional[int] = None
    dmc_id: Optional[int] = None
    base_price: Optional[float] = None
    currency_id: Optional[int] = None
    is_active: bool = True


class PackageCreate(PackageBase):
    items: Optional[List[PackageItemCreate]] = []


class PackageUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    destination: Optional[str] = None
    duration_days: Optional[int] = None
    dmc_id: Optional[int] = None
    base_price: Optional[float] = None
    currency_id: Optional[int] = None
    is_active: Optional[bool] = None


class Package(PackageBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    package_items: List[PackageItem] = []
    
    class Config:
        from_attributes = True


# Hotel Schemas
class HotelBase(BaseModel):
    name: str
    location: str
    star_rating: Optional[int] = None
    amenities: Optional[List[str]] = []
    pricing: Optional[float] = None
    currency_id: Optional[int] = None
    images: Optional[List[str]] = []
    room_types: Optional[Dict[str, Any]] = {}
    description: Optional[str] = None
    dmc_id: Optional[int] = None


class HotelCreate(HotelBase):
    pass


class HotelUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    star_rating: Optional[int] = None
    amenities: Optional[List[str]] = None
    pricing: Optional[float] = None
    currency_id: Optional[int] = None
    images: Optional[List[str]] = None
    room_types: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    dmc_id: Optional[int] = None


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
    currency_id: Optional[int] = None
    category: Optional[str] = None
    time_slots: Optional[List[str]] = []
    images: Optional[List[str]] = []
    dmc_id: Optional[int] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[str] = None
    location: Optional[str] = None
    pricing: Optional[float] = None
    currency_id: Optional[int] = None
    category: Optional[str] = None
    time_slots: Optional[List[str]] = None
    images: Optional[List[str]] = None
    dmc_id: Optional[int] = None


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
    currency_id: Optional[int] = None
    pickup_point: Optional[str] = None
    dropoff_point: Optional[str] = None
    description: Optional[str] = None
    dmc_id: Optional[int] = None


class TransferCreate(TransferBase):
    pass


class TransferUpdate(BaseModel):
    transfer_type: Optional[str] = None
    vehicle_type: Optional[str] = None
    capacity: Optional[int] = None
    pricing: Optional[float] = None
    currency_id: Optional[int] = None
    pickup_point: Optional[str] = None
    dropoff_point: Optional[str] = None
    description: Optional[str] = None
    dmc_id: Optional[int] = None


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
    currency_id: Optional[int] = None
    venue: Optional[str] = None
    description: Optional[str] = None
    dmc_id: Optional[int] = None


class MealCreate(MealBase):
    pass


class MealUpdate(BaseModel):
    meal_type: Optional[str] = None
    cuisine: Optional[str] = None
    dietary_options: Optional[List[str]] = None
    pricing: Optional[float] = None
    currency_id: Optional[int] = None
    venue: Optional[str] = None
    description: Optional[str] = None
    dmc_id: Optional[int] = None


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
    is_optional: bool = False
    option_group: Optional[str] = None
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
    is_optional: Optional[bool] = None
    option_group: Optional[str] = None
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
    currency_id: Optional[int] = None
    package_id: Optional[int] = None


class ItineraryCreate(ItineraryBase):
    items: Optional[List[ItineraryItemCreate]] = []


class ItineraryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    currency_id: Optional[int] = None


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
    base_currency_id: Optional[int] = None
    working_currency_id: Optional[int] = None
    exchange_rate: Optional[Decimal] = None
    converted_price: Optional[float] = None
    markup_percentage: float = 0.0
    dmc_commission: float = 0.0
    pricing_breakdown: Optional[Dict[str, Any]] = {}
    notes: Optional[str] = None


class QuoteCreate(QuoteBase):
    pass


class QuoteUpdate(BaseModel):
    status: Optional[QuoteStatus] = None
    working_currency_id: Optional[int] = None
    markup_percentage: Optional[float] = None
    dmc_commission: Optional[float] = None
    notes: Optional[str] = None


class Quote(QuoteBase):
    id: int
    total_price: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
