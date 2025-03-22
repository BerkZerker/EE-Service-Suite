# Testing Users CRUD API

This document outlines the testing procedure for the Users CRUD API endpoints we've implemented.

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

1. Run Alembic migrations to create tables:
   ```bash
   alembic upgrade head
   ```

2. Create initial admin user:
   ```bash
   python create_admin.py --email=admin@example.com --username=admin --password=adminpassword --full-name="Admin User"
   ```

## Run Automated Tests

Execute the test suite:
```bash
pytest -xvs tests/test_users_api.py
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

4. Test endpoints:
   - GET `/api/users/` - List all users (admin only)
   - POST `/api/users/` - Create a new user (admin only)
   - GET `/api/users/me` - View your profile
   - PUT `/api/users/me` - Update your profile
   - GET `/api/users/{user_id}` - Get user by ID (admin or self)
   - PUT `/api/users/{user_id}` - Update user by ID (admin only)
   - DELETE `/api/users/{user_id}` - Delete user by ID (admin only)

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

Once testing is complete and you've confirmed that the Users CRUD endpoints work correctly, we can move on to implementing the Customers CRUD endpoints.