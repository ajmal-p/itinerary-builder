from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import (
    hotels, activities, transfers, meals, customers, 
    enquiries, itineraries, quotes, currencies, dmcs, packages
)

# Note: Database tables should be created using Alembic migrations
# Run: alembic upgrade head

app = FastAPI(
    title="Itinerary Builder API",
    description="Full-stack itinerary builder application API with multi-currency and DMC support",
    version="2.0.0"
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
app.include_router(currencies.router, prefix="/api/currencies", tags=["Currencies"])
app.include_router(dmcs.router, prefix="/api/dmcs", tags=["DMCs"])
app.include_router(packages.router, prefix="/api/packages", tags=["Packages"])


@app.get("/")
def root():
    return {
        "message": "Welcome to Itinerary Builder API v2.0",
        "features": [
            "Multi-currency support",
            "DMC management",
            "Package templates with options",
            "Automated exchange rate updates"
        ]
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "2.0.0"}
