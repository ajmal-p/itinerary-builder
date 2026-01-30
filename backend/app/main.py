from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import hotels, activities, transfers, meals, customers, enquiries, itineraries, quotes
from app.core.database import engine
from app.models import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Itinerary Builder API",
    description="Full-stack itinerary builder application API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(hotels.router, prefix="/api/hotels", tags=["Hotels"])
app.include_router(activities.router, prefix="/api/activities", tags=["Activities"])
app.include_router(transfers.router, prefix="/api/transfers", tags=["Transfers"])
app.include_router(meals.router, prefix="/api/meals", tags=["Meals"])
app.include_router(customers.router, prefix="/api/customers", tags=["Customers"])
app.include_router(enquiries.router, prefix="/api/enquiries", tags=["Enquiries"])
app.include_router(itineraries.router, prefix="/api/itineraries", tags=["Itineraries"])
app.include_router(quotes.router, prefix="/api/quotes", tags=["Quotes"])


@app.get("/")
def root():
    return {"message": "Welcome to Itinerary Builder API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
