# EE Service Suite - Backend

This is the backend API for the EE Service Suite application, built with FastAPI and SQLAlchemy.

## Features

- **RESTful API**: Complete API for all service management operations
- **Authentication**: JWT token-based with refresh token support
- **Database ORM**: SQLAlchemy models with migration support via Alembic
- **Input Validation**: Pydantic schemas for request/response validation
- **Role-based Access**: Admin and Technician role support
- **Documentation**: Auto-generated API docs with Swagger/ReDoc

## Project Structure

```
backend/
├── alembic/                 # Database migrations
├── app/                     # Application package
│   ├── api/                 # API endpoints
│   │   └── endpoints/       # Route handlers
│   ├── core/                # Core configuration
│   ├── db/                  # Database setup
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   └── services/            # Business logic
├── tests/                   # Test suite
├── alembic.ini              # Alembic configuration
├── main.py                  # Application entry point
└── requirements.txt         # Python dependencies
```

## API Endpoints

The API includes the following major endpoint groups:

- `/api/auth`: Authentication endpoints (login, refresh token)
- `/api/users`: User management
- `/api/customers`: Customer management
- `/api/tickets`: Service ticket operations
- `/api/parts`: Inventory management

## Development

### Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```bash
   alembic upgrade head
   ```

4. Create a test admin user:
   ```bash
   python add_test_user_fixed.py
   ```

### Running

Start the development server:
```bash
uvicorn main:app --reload
```

This will start the server at http://localhost:8000

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run tests with pytest:
```bash
pytest
```

Run specific tests:
```bash
pytest tests/test_users_api.py::test_create_user -v
```

## Authentication

The API uses JWT tokens for authentication. To authenticate:

1. Get a token at `/api/auth/login` with your credentials
2. Include the token in the Authorization header of subsequent requests:
   ```
   Authorization: Bearer <token>
   ```
3. Use `/api/auth/refresh` to get a new access token when needed

## Test Credentials

For testing purposes, use:
- **Email:** admin@example.com
- **Password:** adminpassword