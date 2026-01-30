from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, JSON, Enum, Boolean, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class EnquiryStatus(str, enum.Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    CONVERTED = "converted"
    CLOSED = "closed"


class QuoteStatus(str, enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class ItemType(str, enum.Enum):
    HOTEL = "hotel"
    ACTIVITY = "activity"
    TRANSFER = "transfer"
    MEAL = "meal"


# New models for multi-currency support
class Currency(Base):
    __tablename__ = "currencies"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(3), unique=True, nullable=False, index=True)  # ISO 4217 code (USD, EUR, etc.)
    name = Column(String(100), nullable=False)
    symbol = Column(String(10))
    is_base_currency = Column(Boolean, default=False)  # Library currency
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    exchange_rates_from = relationship("ExchangeRate", foreign_keys="ExchangeRate.from_currency_id", back_populates="from_currency")
    exchange_rates_to = relationship("ExchangeRate", foreign_keys="ExchangeRate.to_currency_id", back_populates="to_currency")


class ExchangeRate(Base):
    __tablename__ = "exchange_rates"
    
    id = Column(Integer, primary_key=True, index=True)
    from_currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=False)
    to_currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=False)
    rate = Column(Numeric(precision=18, scale=6), nullable=False)  # Exchange rate with high precision
    effective_date = Column(DateTime(timezone=True), nullable=False)
    source = Column(String(100))  # API source name
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    from_currency = relationship("Currency", foreign_keys=[from_currency_id], back_populates="exchange_rates_from")
    to_currency = relationship("Currency", foreign_keys=[to_currency_id], back_populates="exchange_rates_to")


# DMC (Destination Management Company) model
class DMC(Base):
    __tablename__ = "dmcs"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False)
    contact_person = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    address = Column(Text)
    destination = Column(String(255))  # Primary destination/location
    commission_percentage = Column(Float, default=0.0)
    payment_terms = Column(Text)
    notes = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    packages = relationship("Package", back_populates="dmc")


# Package model for creating itinerary templates with options
class Package(Base):
    __tablename__ = "packages"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    destination = Column(String(255))
    duration_days = Column(Integer)
    dmc_id = Column(Integer, ForeignKey("dmcs.id"), nullable=True)
    base_price = Column(Float)
    currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    dmc = relationship("DMC", back_populates="packages")
    currency = relationship("Currency")
    package_items = relationship("PackageItem", back_populates="package", cascade="all, delete-orphan")


class PackageItem(Base):
    __tablename__ = "package_items"
    
    id = Column(Integer, primary_key=True, index=True)
    package_id = Column(Integer, ForeignKey("packages.id"), nullable=False)
    day_number = Column(Integer, nullable=False)
    item_type = Column(Enum(ItemType), nullable=False)
    item_order = Column(Integer, default=0)
    is_optional = Column(Boolean, default=False)
    option_group = Column(String(100))  # Group multiple options together (e.g., "hotel_options_day1")
    
    # Foreign keys for different item types
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=True)
    transfer_id = Column(Integer, ForeignKey("transfers.id"), nullable=True)
    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=True)
    
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    package = relationship("Package", back_populates="package_items")
    hotel = relationship("Hotel")
    activity = relationship("Activity")
    transfer = relationship("Transfer")
    meal = relationship("Meal")


class Hotel(Base):
    __tablename__ = "hotels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    star_rating = Column(Integer)
    amenities = Column(JSON)  # List of amenities
    pricing = Column(Float)
    currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=True)  # Multi-currency support
    images = Column(JSON)  # List of image URLs
    room_types = Column(JSON)  # Room configurations
    description = Column(Text)
    dmc_id = Column(Integer, ForeignKey("dmcs.id"), nullable=True)  # DMC association
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    currency = relationship("Currency")
    dmc = relationship("DMC")
    itinerary_items = relationship("ItineraryItem", back_populates="hotel")


class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    duration = Column(String(100))  # e.g., "2 hours", "half day"
    location = Column(String(255))
    pricing = Column(Float)
    currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=True)  # Multi-currency support
    category = Column(String(100))
    time_slots = Column(JSON)  # Available time slots
    images = Column(JSON)
    dmc_id = Column(Integer, ForeignKey("dmcs.id"), nullable=True)  # DMC association
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    currency = relationship("Currency")
    dmc = relationship("DMC")
    itinerary_items = relationship("ItineraryItem", back_populates="activity")


class Transfer(Base):
    __tablename__ = "transfers"
    
    id = Column(Integer, primary_key=True, index=True)
    transfer_type = Column(String(100), nullable=False)  # airport, city, inter-city
    vehicle_type = Column(String(100))
    capacity = Column(Integer)
    pricing = Column(Float)
    currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=True)  # Multi-currency support
    pickup_point = Column(String(255))
    dropoff_point = Column(String(255))
    description = Column(Text)
    dmc_id = Column(Integer, ForeignKey("dmcs.id"), nullable=True)  # DMC association
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    currency = relationship("Currency")
    dmc = relationship("DMC")
    itinerary_items = relationship("ItineraryItem", back_populates="transfer")


class Meal(Base):
    __tablename__ = "meals"
    
    id = Column(Integer, primary_key=True, index=True)
    meal_type = Column(String(100), nullable=False)  # breakfast, lunch, dinner
    cuisine = Column(String(100))
    dietary_options = Column(JSON)  # List of dietary options
    pricing = Column(Float)
    currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=True)  # Multi-currency support
    venue = Column(String(255))  # Restaurant/venue name
    description = Column(Text)
    dmc_id = Column(Integer, ForeignKey("dmcs.id"), nullable=True)  # DMC association
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    currency = relationship("Currency")
    dmc = relationship("DMC")
    itinerary_items = relationship("ItineraryItem", back_populates="meal")


class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(50))
    preferences = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    enquiries = relationship("Enquiry", back_populates="customer")


class Enquiry(Base):
    __tablename__ = "enquiries"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    status = Column(Enum(EnquiryStatus), default=EnquiryStatus.NEW)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    customer = relationship("Customer", back_populates="enquiries")
    quotes = relationship("Quote", back_populates="enquiry")


class Itinerary(Base):
    __tablename__ = "itineraries"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    total_price = Column(Float, default=0.0)
    currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=True)  # Base currency for itinerary
    package_id = Column(Integer, ForeignKey("packages.id"), nullable=True)  # Link to package if created from one
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    currency = relationship("Currency")
    package = relationship("Package")
    items = relationship("ItineraryItem", back_populates="itinerary", cascade="all, delete-orphan")
    quotes = relationship("Quote", back_populates="itinerary")


class ItineraryItem(Base):
    __tablename__ = "itinerary_items"
    
    id = Column(Integer, primary_key=True, index=True)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id"), nullable=False)
    day_number = Column(Integer, nullable=False)
    item_type = Column(Enum(ItemType), nullable=False)
    item_order = Column(Integer, default=0)  # Order within the day
    is_optional = Column(Boolean, default=False)  # For package options
    option_group = Column(String(100))  # Group alternatives together
    
    # Foreign keys for different item types
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=True)
    transfer_id = Column(Integer, ForeignKey("transfers.id"), nullable=True)
    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=True)
    
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    itinerary = relationship("Itinerary", back_populates="items")
    hotel = relationship("Hotel", back_populates="itinerary_items")
    activity = relationship("Activity", back_populates="itinerary_items")
    transfer = relationship("Transfer", back_populates="itinerary_items")
    meal = relationship("Meal", back_populates="itinerary_items")


class Quote(Base):
    __tablename__ = "quotes"
    
    id = Column(Integer, primary_key=True, index=True)
    enquiry_id = Column(Integer, ForeignKey("enquiries.id"), nullable=False)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id"), nullable=False)
    status = Column(Enum(QuoteStatus), default=QuoteStatus.DRAFT)
    base_price = Column(Float)
    base_currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=True)  # Library currency
    working_currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=True)  # Quote currency
    exchange_rate = Column(Numeric(precision=18, scale=6))  # Rate used for conversion
    converted_price = Column(Float)  # Price in working currency
    markup_percentage = Column(Float, default=0.0)
    dmc_commission = Column(Float, default=0.0)  # DMC commission amount
    total_price = Column(Float)
    pricing_breakdown = Column(JSON)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    enquiry = relationship("Enquiry", back_populates="quotes")
    itinerary = relationship("Itinerary", back_populates="quotes")
    base_currency = relationship("Currency", foreign_keys=[base_currency_id])
    working_currency = relationship("Currency", foreign_keys=[working_currency_id])
