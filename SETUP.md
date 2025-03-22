# EE Service Suite - Setup Guide

## Prerequisites

- Python 3.9+ (for backend)
- Node.js 18+ (for frontend)
- npm or yarn (for frontend package management)

## Backend Setup

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

## Frontend Setup

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