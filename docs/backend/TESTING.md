# Testing Guide

This document outlines the testing strategies and procedures for the EE Service Suite backend.

## Testing Stack

- **Test Framework**: pytest
- **HTTP Client**: httpx for async API testing
- **Database**: In-memory SQLite for unit tests
- **Fixtures**: pytest fixtures for reusable test components

## Test Types

### Unit Tests

Unit tests focus on testing individual functions and methods in isolation:

- Core utility functions
- Authentication logic
- Data validation

### Integration Tests

Integration tests verify that components work together correctly:

- API endpoints
- Database interactions
- Authentication flows

### End-to-End Tests

E2E tests validate complete user flows:

- Creating and managing tickets
- Customer registration and update
- Parts inventory management

## Running Tests

### Running All Tests

```bash
pytest
```

### Running Specific Test Files

```bash
pytest tests/test_users_api.py
```

### Running Specific Test Functions

```bash
pytest tests/test_users_api.py::test_create_user -v
```

### Running Tests with Coverage

```bash
pytest --cov=app tests/
```

## Test Configuration

Tests use a separate in-memory SQLite database to avoid affecting the development or production database.

## Authentication in Tests

Many tests require authentication. The test suite includes fixtures for creating test users and generating authentication tokens:

```python
def test_protected_route(client, admin_token_headers):
    response = client.get("/api/users/", headers=admin_token_headers)
    assert response.status_code == 200
```

## Test Data

Test fixtures create the necessary data for tests:

- Test users (admin and regular)
- Sample customers
- Sample tickets
- Sample inventory items

## Manual Testing

For manual testing, use the following credentials:

- **Email:** admin@example.com
- **Password:** adminpassword

The API documentation is available at:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)