# Testing Backend API

This document outlines the testing procedure for the API endpoints. We now have two fully implemented and tested API modules.

## Implementation Status

✅ **Users CRUD API**: Fully implemented with:
- Complete CRUD operations (Create, Read, Update, Delete)
- Role-based access control (Admin vs. Technician)
- JWT token authentication
- Comprehensive test coverage (12 test cases, all passing)
- Proper permission checks and error handling

✅ **Customers CRUD API**: Fully implemented with:
- Complete CRUD operations (Create, Read, Update, Delete)
- Search functionality with case-insensitive matching
- Filtering by name, email, or phone
- Relationship with bikes (get customer with associated bikes)
- Comprehensive test coverage (9 test cases, all passing)
- Role-based permission control (admin-only for deletions)

## Setup Environment

1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install requirements:
   ```bash
   pip install -r requirements.txt
   
   # Ensure bcrypt is installed (needed for password hashing)
   pip install bcrypt
   ```

3. Make sure `.env` file is created with:
   ```
   DATABASE_URL=sqlite:///./ee_service.db
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

## Initialize Database

### Production Database

The application uses a SQLite database with the following characteristics:
- **File location**: `/app/app.db` in the Docker container, or `./backend/app.db` locally
- **Configuration**: Set via the `DATABASE_URL` environment variable in `docker-compose.yml`
- **Persistence**: The database is fully persistent and preserved across container restarts
- **Schema**: Contains all application tables (users, customers, bikes, tickets, parts, etc.)
- **Migration management**: Managed by Alembic for version control

### Test Database

For automated tests, we use:
- Isolated in-memory SQLite databases (`:memory:`)
- Completely separate from the production database
- Automatically created/destroyed for each test run
- No impact on production data

### Setup Steps

1. Run Alembic migrations to create tables:
   ```bash
   alembic upgrade head
   ```

2. Create initial admin user:
   ```bash
   python create_admin.py --email=admin@example.com --username=admin --password=adminpassword --full-name="Admin User"
   ```

## Run Automated Tests

Execute the test suites:
```bash
# Test Users API
pytest -xvs tests/test_users_api.py

# Test Customers API
pytest -xvs tests/test_customers_api.py
```

## Manual API Testing

1. Start FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

2. Access the Swagger UI at http://localhost:8000/docs

3. Authentication flow:
   - Use `/api/auth/login` endpoint with admin credentials to get a token
   - Click the "Authorize" button at the top right and enter the token

4. Test Users API endpoints:
   - GET `/api/users/` - List all users (admin only)
   - POST `/api/users/` - Create a new user (admin only)
   - GET `/api/users/me` - View your profile
   - PUT `/api/users/me` - Update your profile
   - GET `/api/users/{user_id}` - Get user by ID (admin or self)
   - PUT `/api/users/{user_id}` - Update user by ID (admin only)
   - DELETE `/api/users/{user_id}` - Delete user by ID (admin only)

5. Test Customers API endpoints:
   - GET `/api/customers/` - List all customers (with optional filtering)
   - POST `/api/customers/` - Create a new customer
   - GET `/api/customers/{customer_id}` - Get customer by ID
   - GET `/api/customers/{customer_id}/with-bikes` - Get customer with bikes
   - PUT `/api/customers/{customer_id}` - Update customer
   - DELETE `/api/customers/{customer_id}` - Delete customer (admin only)
   - GET `/api/customers/search/?search_term=...` - Search customers by name/email/phone

## Permission Tests

Test with both admin and regular user accounts to verify:
- Regular users can only access/modify their own profiles
- Admin users can access/modify all users
- Authentication is required for all endpoints
- Proper error responses for unauthorized access

## Data Validation Tests

- Test email uniqueness constraint
- Test username uniqueness constraint 
- Test password hashing
- Test invalid input handling

## After Testing

All tests for both API modules are now passing.

### Users API Notes
A key bugfix was implemented to ensure proper permission handling:
- When a non-admin user attempts to access another user's profile, the API now correctly returns a 403 Forbidden response instead of 404 Not Found
- Permission checks are now performed before checking if a user exists, ensuring proper security

### Customers API Notes
The Customers API includes:
- Search functionality with partial matching for name, email, and phone fields
- Integration with bikes model (relationship between customers and bikes)
- Proper error handling for non-existent resources
- Role-based permissions (only admins can delete customers)

With both the Users and Customers CRUD APIs complete, we can now move on to implementing the Tickets CRUD endpoints, which is the next priority according to the project plan.

## Technical Debt Notes

We've addressed several deprecated patterns in our codebase:

1. ✅ Updated SQLAlchemy `declarative_base()` to use the proper import location
2. ✅ Updated User schema to use Pydantic V2 style `model_config` instead of class-based Config
3. ✅ Updated Customer schema to use Pydantic V2 style `model_config` with `from_attributes = True`
4. ✅ Updated Bike schema to use Pydantic V2 style `model_config` with `from_attributes = True`
5. ⏳ Other schema files still need to be updated to the new configuration style:
   - service.py
   - ticket.py
   - ticket_part.py
   - part.py
   - ticket_update.py

We've also improved the API documentation by:
1. ✅ Adding OpenAPI documentation to all endpoints with `summary` and `description` fields
2. ✅ Adding detailed docstrings for all API functions
3. ✅ Documenting parameters, return values, and error cases in each endpoint

These changes enhance the developer experience and make API exploration through Swagger UI more user-friendly.

The remaining schema updates will be completed as part of the Tickets CRUD implementation.