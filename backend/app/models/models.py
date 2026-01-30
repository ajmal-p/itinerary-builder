from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, JSON, Enum
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


class Hotel(Base):
    __tablename__ = "hotels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    star_rating = Column(Integer)
    amenities = Column(JSON)  # List of amenities
    pricing = Column(Float)
    images = Column(JSON)  # List of image URLs
    room_types = Column(JSON)  # Room configurations
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    itinerary_items = relationship("ItineraryItem", back_populates="hotel")


class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    duration = Column(String(100))  # e.g., "2 hours", "half day"
    location = Column(String(255))
    pricing = Column(Float)
    category = Column(String(100))
    time_slots = Column(JSON)  # Available time slots
    images = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    itinerary_items = relationship("ItineraryItem", back_populates="activity")


class Transfer(Base):
    __tablename__ = "transfers"
    
    id = Column(Integer, primary_key=True, index=True)
    transfer_type = Column(String(100), nullable=False)  # airport, city, inter-city
    vehicle_type = Column(String(100))
    capacity = Column(Integer)
    pricing = Column(Float)
    pickup_point = Column(String(255))
    dropoff_point = Column(String(255))
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    itinerary_items = relationship("ItineraryItem", back_populates="transfer")


class Meal(Base):
    __tablename__ = "meals"
    
    id = Column(Integer, primary_key=True, index=True)
    meal_type = Column(String(100), nullable=False)  # breakfast, lunch, dinner
    cuisine = Column(String(100))
    dietary_options = Column(JSON)  # List of dietary options
    pricing = Column(Float)
    venue = Column(String(255))  # Restaurant/venue name
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
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
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    items = relationship("ItineraryItem", back_populates="itinerary", cascade="all, delete-orphan")
    quotes = relationship("Quote", back_populates="itinerary")


class ItineraryItem(Base):
    __tablename__ = "itinerary_items"
    
    id = Column(Integer, primary_key=True, index=True)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id"), nullable=False)
    day_number = Column(Integer, nullable=False)
    item_type = Column(Enum(ItemType), nullable=False)
    item_order = Column(Integer, default=0)  # Order within the day
    
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
    markup_percentage = Column(Float, default=0.0)
    total_price = Column(Float)
    pricing_breakdown = Column(JSON)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    enquiry = relationship("Enquiry", back_populates="quotes")
    itinerary = relationship("Itinerary", back_populates="quotes")
