# EE Service Suite - Setup Guide

## Prerequisites

- Python 3.9+ (for backend)
- Node.js 18+ (for frontend)
- npm or yarn (for frontend package management)
- Docker and Docker Compose (for containerized setup)

## Setup Options

### Option 1: Docker Setup (Recommended)

1. Ensure Docker and Docker Compose are installed on your system.

2. Create a `.env` file in the backend directory based on the `.env.example` template:
   ```
   cp backend/.env.example backend/.env
   ```

3. Build and start the containers:
   ```
   docker-compose up -d
   ```

4. Setup the database (first time only):
   ```
   # If you're using Docker Compose V2, use this command:
   docker compose exec backend alembic upgrade head
   
   # For older Docker Compose versions:
   docker-compose exec backend alembic upgrade head
   ```

5. Access the services:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

To stop the services:
```
docker-compose down
```

### Option 2: Local Development Setup

#### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Set up the database:
   ```
   # Apply the initial migration
   alembic upgrade head
   
   # For future migrations, create and apply
   # alembic revision --autogenerate -m "migration description"
   # alembic upgrade head
   ```

6. Run the development server:
   ```
   uvicorn main:app --reload
   ```

The backend will be available at http://localhost:8000, and the API documentation at http://localhost:8000/docs.

#### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   # or
   yarn
   ```

3. Run the development server:
   ```
   npm run dev
   # or
   yarn dev
   ```

The frontend will be available at http://localhost:5173.

## Development Workflow

1. Run both the backend and frontend development servers.
2. The frontend is configured to proxy API requests to the backend.
3. Make changes to the code, and the servers will automatically reload.

## API Development Priorities

In accordance with our project plan, API endpoints will be developed in the following order:

1. **Users CRUD** (staff accounts) - Essential for authentication and service tracking
2. **Customers CRUD** - With logic for automatic creation during ticket creation
3. **Tickets CRUD** - With customer lookup/creation integration
4. **Bikes CRUD** - Implemented as a subsection of customers
5. **Parts CRUD** - Lowest priority, to be implemented after core service functionality

This priority order creates a logical workflow where:
- Staff users are created first (authentication foundation)
- Customer management is implemented second
- Ticket creation with customer integration follows
- Bikes are managed as a hierarchical relationship under customers
- Parts/inventory is implemented last after core functionality is in place