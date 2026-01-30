# Itinerary Builder

A full-stack itinerary builder application with React frontend and FastAPI backend.

## Project Overview

This is a comprehensive travel itinerary management system that allows you to:
- Manage hotels, activities, transfers, and meals
- Create detailed itineraries by combining these elements
- Track customers and their enquiries
- Generate quotes with pricing breakdowns
- Export quotes as PDF documents

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Relational database
- **SQLAlchemy**: ORM for database operations
- **Alembic**: Database migrations
- **Pydantic**: Data validation
- **ReportLab**: PDF generation

### Frontend
- **React**: UI library
- **React Router**: Navigation
- **Material-UI**: Component library
- **Axios**: HTTP client
- **Context API**: State management

## Project Structure

```
itinerary-builder/
├── backend/
│   ├── app/
│   │   ├── api/endpoints/    # API route handlers
│   │   ├── models/           # Database models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── crud/             # CRUD operations
│   │   ├── core/             # Core functionality
│   │   └── main.py           # FastAPI app
│   ├── alembic/              # Database migrations
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   ├── store/           # State management
│   │   └── App.js
│   ├── package.json
│   └── README.md
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- PostgreSQL 12+

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp .env.example .env
```

5. Update `.env` with your PostgreSQL credentials:
```
DATABASE_URL=postgresql://user:password@localhost:5432/itinerary_db
SECRET_KEY=your-secret-key
```

6. Create the database:
```bash
createdb itinerary_db
```

7. Run migrations:
```bash
alembic upgrade head
```

8. Start the backend server:
```bash
uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file:
```bash
cp .env.example .env
```

4. Start the development server:
```bash
npm start
```

Frontend will be available at `http://localhost:3000`

## Features

### Module Management
- **Hotels**: Add, edit, delete hotels with details like location, star rating, amenities, and pricing
- **Activities**: Manage activities with duration, category, and time slots
- **Transfers**: Track transportation options with vehicle types and capacity
- **Meals**: Manage meal packages with cuisine types and dietary options

### Itinerary Builder
- Create multi-day itineraries
- Add items (hotels, activities, transfers, meals) day-by-day
- Drag-and-drop interface for organizing items
- Automatic pricing calculation
- Timeline view of the itinerary

### Customer & Enquiry Management
- Customer database with contact information
- Track enquiries linked to customers
- Enquiry status management (new, in-progress, converted, closed)

### Quote System
- Generate quotes from itineraries
- Apply markup percentages to base prices
- Pricing breakdown
- Export quotes as PDF
- Quote status tracking (draft, sent, accepted, rejected)

## API Endpoints

### Hotels
- `GET /api/hotels` - List all hotels
- `POST /api/hotels` - Create hotel
- `GET /api/hotels/{id}` - Get hotel details
- `PUT /api/hotels/{id}` - Update hotel
- `DELETE /api/hotels/{id}` - Delete hotel

### Activities
- `GET /api/activities` - List all activities
- `POST /api/activities` - Create activity
- `GET /api/activities/{id}` - Get activity details
- `PUT /api/activities/{id}` - Update activity
- `DELETE /api/activities/{id}` - Delete activity

### Transfers
- `GET /api/transfers` - List all transfers
- `POST /api/transfers` - Create transfer
- `GET /api/transfers/{id}` - Get transfer details
- `PUT /api/transfers/{id}` - Update transfer
- `DELETE /api/transfers/{id}` - Delete transfer

### Meals
- `GET /api/meals` - List all meals
- `POST /api/meals` - Create meal
- `GET /api/meals/{id}` - Get meal details
- `PUT /api/meals/{id}` - Update meal
- `DELETE /api/meals/{id}` - Delete meal

### Customers
- `GET /api/customers` - List all customers
- `POST /api/customers` - Create customer
- `GET /api/customers/{id}` - Get customer details
- `PUT /api/customers/{id}` - Update customer
- `DELETE /api/customers/{id}` - Delete customer

### Enquiries
- `GET /api/enquiries` - List all enquiries
- `POST /api/enquiries` - Create enquiry
- `GET /api/enquiries/{id}` - Get enquiry details
- `GET /api/enquiries/customer/{customer_id}` - Get customer enquiries
- `PUT /api/enquiries/{id}` - Update enquiry
- `DELETE /api/enquiries/{id}` - Delete enquiry

### Itineraries
- `GET /api/itineraries` - List all itineraries
- `POST /api/itineraries` - Create itinerary
- `GET /api/itineraries/{id}` - Get itinerary details
- `PUT /api/itineraries/{id}` - Update itinerary
- `DELETE /api/itineraries/{id}` - Delete itinerary
- `POST /api/itineraries/{id}/items` - Add item to itinerary
- `GET /api/itineraries/{id}/items` - Get itinerary items
- `PUT /api/itineraries/items/{item_id}` - Update itinerary item
- `DELETE /api/itineraries/items/{item_id}` - Delete itinerary item

### Quotes
- `GET /api/quotes` - List all quotes
- `POST /api/quotes` - Create quote
- `GET /api/quotes/{id}` - Get quote details
- `GET /api/quotes/enquiry/{enquiry_id}` - Get enquiry quotes
- `PUT /api/quotes/{id}` - Update quote
- `DELETE /api/quotes/{id}` - Delete quote
- `GET /api/quotes/{id}/pdf` - Export quote as PDF

## Database Schema

The application uses the following main tables:
- `hotels` - Hotel information
- `activities` - Activity details
- `transfers` - Transfer options
- `meals` - Meal packages
- `customers` - Customer information
- `enquiries` - Customer enquiries
- `itineraries` - Main itinerary records
- `itinerary_items` - Items within itineraries
- `quotes` - Quote information

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.
