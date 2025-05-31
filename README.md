# Full Stack Dashboard

A modern investment portfolio dashboard built with Next.js, FastAPI, and PostgreSQL.

## Tech Stack

### Frontend
- Next.js 13+ (React)
- TailwindCSS for styling
- Recharts for data visualization
- React Query for state management
- TypeScript for type safety

### Backend
- FastAPI (Python)
- PostgreSQL with Supabase
- JWT Authentication
- SQLAlchemy ORM

### Deployment
- Frontend: Vercel
- Backend: Render/Railway
- Database: Supabase

## Features

- 📊 Interactive portfolio dashboard
- 📈 Real-time investment tracking
- 🔐 Secure authentication
- 📱 Responsive design
- 📊 Advanced data visualization
- 🔄 Real-time data updates
- 🎨 Modern UI/UX

## Setup Instructions

### Prerequisites
- Node.js 16+
- Python 3.8+
- PostgreSQL
- npm or yarn

### Frontend Setup
```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload
```

### Environment Variables
Create `.env` files in both frontend and backend directories:

Frontend (.env):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Backend (.env):
```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key
```

## API Documentation
API documentation is available at `/docs` when running the backend server.

## Database Schema
The database includes tables for:
- Users
- Portfolios
- Investments
- Mutual Funds
- Transactions
- Sectors
- Stocks

## Deployment
1. Frontend: Deploy to Vercel
2. Backend: Deploy to Render/Railway
3. Database: Set up on Supabase

## Additional Notes
- The project uses TypeScript for better type safety
- Implements proper error handling and logging
- Uses efficient database queries with proper indexing
- Follows REST API best practices
- Implements JWT authentication for security

## License
MIT 