# Itinerary Builder - Quick Start Guide

## Prerequisites
- Docker and Docker Compose (recommended for easiest setup)
- OR Python 3.8+, Node.js 14+, and PostgreSQL 12+

## Quick Start with Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/ajmal-p/itinerary-builder.git
cd itinerary-builder
```

2. Create environment file:
```bash
echo "SECRET_KEY=your-secret-key-$(openssl rand -hex 32)" > .env
```

3. Start all services:
```bash
docker-compose up -d
```

4. Access the applications:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

5. Stop services:
```bash
docker-compose down
```

## Manual Setup (Without Docker)

### Backend Setup

1. Create and activate virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

4. Setup database:
```bash
# Create database
createdb itinerary_db

# Run migrations
alembic upgrade head
```

5. Start backend server:
```bash
uvicorn app.main:app --reload
```

Backend will be available at http://localhost:8000

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env if your backend is not at http://localhost:8000
```

3. Start development server:
```bash
npm start
```

Frontend will be available at http://localhost:3000

## First Steps

### 1. Add Resources
Start by adding basic resources:
- Navigate to Hotels, Activities, Transfers, or Meals
- Click "Add" button
- Fill in the details and save

### 2. Create Customers
- Go to Customers page
- Add customer information
- Customers can be linked to enquiries

### 3. Build Itineraries
- Navigate to Itineraries
- Click "Create Itinerary"
- Add items day by day
- Save your itinerary

### 4. Generate Quotes
- Go to Quotes page
- Create a new quote
- Link it to an enquiry and itinerary
- Export as PDF

## Database Schema

The application uses the following main tables:
- **hotels**: Hotel information with amenities and pricing
- **activities**: Activities with duration and categories
- **transfers**: Transfer options with vehicle details
- **meals**: Meal packages with dietary options
- **customers**: Customer contact information
- **enquiries**: Customer enquiries with status tracking
- **itineraries**: Main itinerary records
- **itinerary_items**: Items within itineraries (links to hotels, activities, etc.)
- **quotes**: Quote information with pricing breakdown

## API Endpoints Overview

### Core Modules
- **Hotels**: `/api/hotels`
- **Activities**: `/api/activities`
- **Transfers**: `/api/transfers`
- **Meals**: `/api/meals`

### Customer Management
- **Customers**: `/api/customers`
- **Enquiries**: `/api/enquiries`

### Itinerary System
- **Itineraries**: `/api/itineraries`
- **Itinerary Items**: `/api/itineraries/{id}/items`

### Quote System
- **Quotes**: `/api/quotes`
- **PDF Export**: `/api/quotes/{id}/pdf`

## Frontend Routes

- `/` - Home page
- `/hotels` - Hotels management
- `/activities` - Activities management
- `/transfers` - Transfers list
- `/meals` - Meals list
- `/customers` - Customers management
- `/enquiries` - Enquiries list
- `/itineraries` - Itineraries list
- `/itineraries/new` - Create new itinerary
- `/itineraries/:id` - Edit itinerary
- `/quotes` - Quotes list

## Production Deployment

### Backend Production Settings

1. Update `.env` with production values:
```env
DATABASE_URL=postgresql://prod_user:strong_password@prod_host:5432/prod_db
SECRET_KEY=<generate-strong-secret-key>
```

2. Build for production:
```bash
# Run migrations
alembic upgrade head

# Start with gunicorn (install first: pip install gunicorn)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend Production Build

1. Update `.env` with production API URL:
```env
REACT_APP_API_URL=https://your-api-domain.com/api
```

2. Build for production:
```bash
npm run build
```

3. Serve the `build` folder with a web server (nginx, Apache, etc.)

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check DATABASE_URL in `.env`
- Verify database exists and migrations are run

### Frontend Not Connecting to Backend
- Check REACT_APP_API_URL in frontend `.env`
- Ensure backend is running and accessible
- Check browser console for CORS errors

### API Documentation
Visit http://localhost:8000/docs for interactive API documentation

## Support

For issues or questions:
- Check the README.md in backend and frontend directories
- Review API documentation at /docs endpoint
- Check GitHub issues

## License
MIT License
