# Setup Guide

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/downloads) (for development)
- [Node.js](https://nodejs.org/) v16+ and npm (for local development)
- [Python](https://www.python.org/downloads/) 3.9+ and pip (for local development)

## Quick Start (Docker)

The recommended way to run the application is using Docker:

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/ee-service-suite.git
   cd ee-service-suite
   ```

2. Start the application:
   ```bash
   docker-compose up -d
   ```

3. Access the application:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. Login with the test admin account:
   - Email: admin@example.com
   - Password: adminpassword

## Development Setup

### Backend (FastAPI)

1. Create a virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run database migrations:
   ```bash
   alembic upgrade head
   ```

4. Create an admin user and test data:
   ```bash
   python3 setup_test_data.py
   ```
   
   This script provides several options:
   ```bash
   # Reset database and create fresh test data
   python3 setup_test_data.py --reset
   
   # Only fix enum values in database (if you have issues with tickets not showing)
   python3 setup_test_data.py --fix-enums
   ```

5. Start the development server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend (React)

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

## Testing

### Backend Tests

Run the test suite:
```bash
cd backend
pytest
```

Run a specific test:
```bash
pytest tests/test_users_api.py::test_create_user -v
```

### Frontend Tests

Run the test suite:
```bash
cd frontend
npm test
```

## Environment Variables

The application uses the following environment variables which can be set in a `.env` file:

### Backend

- `SECRET_KEY`: JWT secret key
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiration (default: 30)
- `DATABASE_URL`: SQLite database URL (default: sqlite:///./app.db)

### Frontend

- `VITE_API_URL`: API URL (default: http://localhost:8000)

## Backup Setup

By default, the SQLite database file is stored in the backend directory. To set up automated backups:

1. Create a Dropbox app and get an access token
2. Add the access token to your environment variables:
   ```
   DROPBOX_ACCESS_TOKEN=your_access_token
   ```

3. Run the backup script (can be scheduled as a cron job):
   ```bash
   python backend/scripts/backup.py
   ```

## Troubleshooting

### Common Issues

- If the frontend can't connect to the backend, check that the API URL is correctly set
- If database migrations fail, try removing the alembic version table and rerunning migrations
- For permission issues with SQLite, check file permissions on the database file

### Logs

- Backend logs: `docker-compose logs backend`
- Frontend logs: `docker-compose logs frontend`

## Updating

To update the application:

1. Pull the latest changes:
   ```bash
   git pull
   ```

2. Rebuild the containers:
   ```bash
   docker-compose build
   docker-compose up -d
   ```

3. Run any new migrations:
   ```bash
   docker-compose exec backend alembic upgrade head
   ```