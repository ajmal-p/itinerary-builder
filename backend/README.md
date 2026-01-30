# Backend - Itinerary Builder API

FastAPI backend for the itinerary builder application.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

3. Update the `.env` file with your PostgreSQL database credentials.

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

## API Endpoints

### Hotels
- `POST /api/hotels` - Create hotel
- `GET /api/hotels` - List hotels
- `GET /api/hotels/{id}` - Get hotel
- `PUT /api/hotels/{id}` - Update hotel
- `DELETE /api/hotels/{id}` - Delete hotel

### Activities
- `POST /api/activities` - Create activity
- `GET /api/activities` - List activities
- `GET /api/activities/{id}` - Get activity
- `PUT /api/activities/{id}` - Update activity
- `DELETE /api/activities/{id}` - Delete activity

### Transfers
- `POST /api/transfers` - Create transfer
- `GET /api/transfers` - List transfers
- `GET /api/transfers/{id}` - Get transfer
- `PUT /api/transfers/{id}` - Update transfer
- `DELETE /api/transfers/{id}` - Delete transfer

### Meals
- `POST /api/meals` - Create meal
- `GET /api/meals` - List meals
- `GET /api/meals/{id}` - Get meal
- `PUT /api/meals/{id}` - Update meal
- `DELETE /api/meals/{id}` - Delete meal

### Customers
- `POST /api/customers` - Create customer
- `GET /api/customers` - List customers
- `GET /api/customers/{id}` - Get customer
- `PUT /api/customers/{id}` - Update customer
- `DELETE /api/customers/{id}` - Delete customer

### Enquiries
- `POST /api/enquiries` - Create enquiry
- `GET /api/enquiries` - List enquiries
- `GET /api/enquiries/{id}` - Get enquiry
- `GET /api/enquiries/customer/{customer_id}` - Get customer enquiries
- `PUT /api/enquiries/{id}` - Update enquiry
- `DELETE /api/enquiries/{id}` - Delete enquiry

### Itineraries
- `POST /api/itineraries` - Create itinerary
- `GET /api/itineraries` - List itineraries
- `GET /api/itineraries/{id}` - Get itinerary
- `PUT /api/itineraries/{id}` - Update itinerary
- `DELETE /api/itineraries/{id}` - Delete itinerary
- `POST /api/itineraries/{id}/items` - Add item to itinerary
- `GET /api/itineraries/{id}/items` - Get itinerary items
- `PUT /api/itineraries/items/{item_id}` - Update itinerary item
- `DELETE /api/itineraries/items/{item_id}` - Delete itinerary item

### Quotes
- `POST /api/quotes` - Create quote
- `GET /api/quotes` - List quotes
- `GET /api/quotes/{id}` - Get quote
- `GET /api/quotes/enquiry/{enquiry_id}` - Get enquiry quotes
- `PUT /api/quotes/{id}` - Update quote
- `DELETE /api/quotes/{id}` - Delete quote
- `GET /api/quotes/{id}/pdf` - Export quote as PDF
