# Troubleshooting Guide

This document provides solutions to common issues you might encounter when running the EE Service Suite.

## Docker Issues

### Containers Not Starting

**Problem:** Docker containers fail to start or exit immediately after starting.

**Solution:**
1. Check container logs:
   ```bash
   docker-compose logs frontend
   docker-compose logs backend
   ```
2. Ensure ports are not already in use:
   ```bash
   lsof -i :5173
   lsof -i :8000
   ```
3. Verify Docker is running properly:
   ```bash
   docker info
   ```

### Volume Mounting Issues

**Problem:** Changes to code aren't reflected in the running containers.

**Solution:**
1. Rebuild the containers:
   ```bash
   docker-compose down
   docker-compose up -d --build
   ```
2. Check volume mounts in docker-compose.yml
3. Ensure file paths are correct for your operating system

## Frontend Issues

### Can't Access Frontend

**Problem:** Unable to access the frontend at http://localhost:5173.

**Solution:**
1. Verify the frontend container is running:
   ```bash
   docker ps | grep frontend
   ```
2. Check the frontend logs for errors:
   ```bash
   docker-compose logs frontend
   ```
3. Try accessing with different browser or incognito mode
4. If using WSL, try accessing via 127.0.0.1 instead of localhost

### Authentication Issues

**Problem:** Can't login or getting authentication errors.

**Solution:**
1. Verify you're using the correct credentials:
   - Email: admin@example.com
   - Password: adminpassword
2. Check that the backend is accessible at http://localhost:8000/docs
3. Clear browser cookies and localStorage
4. Make sure the backend container is running

## Backend Issues

### Database Migration Errors

**Problem:** Alembic migrations fail to apply.

**Solution:**
1. Reset the database (development only):
   ```bash
   docker-compose exec backend rm app.db
   docker-compose exec backend alembic upgrade head
   docker-compose exec backend python add_test_user_fixed.py
   ```
2. Check alembic version table for conflicts
3. Review migration scripts for errors

### API Endpoint Errors

**Problem:** API endpoints return unexpected errors.

**Solution:**
1. Check the request format against the API documentation
2. Verify authorization headers are correct
3. Check backend logs for detailed error messages:
   ```bash
   docker-compose logs backend
   ```

## Development Environment Issues

### Package Installation Problems

**Problem:** npm or pip fail to install packages.

**Solution:**
1. Clear package caches:
   ```bash
   npm cache clean --force
   pip cache purge
   ```
2. Update package managers:
   ```bash
   npm install -g npm
   pip install --upgrade pip
   ```
3. Check for version conflicts in package.json or requirements.txt

### Linting or Type Checking Errors

**Problem:** ESLint, flake8, or TypeScript errors.

**Solution:**
1. Run linters/type checkers locally to see detailed errors:
   ```bash
   # Frontend
   cd frontend
   npm run lint
   npm run typecheck
   
   # Backend
   cd backend
   flake8
   mypy .
   ```
2. Check configuration files for linting rules

## Restoring from Backup

If you need to restore from a backup:

1. Stop the containers:
   ```bash
   docker-compose down
   ```

2. Replace the database file with the backup:
   ```bash
   cp backup/app.db.backup backend/app.db
   ```

3. Restart the containers:
   ```bash
   docker-compose up -d
   ```

## Common Error Messages

### "Incorrect email or password"

Ensure you're using the correct test credentials:
- Email: admin@example.com
- Password: adminpassword

### "Network error: Failed to fetch"

This usually indicates the backend is not accessible. Check that the backend container is running and that the API URL is correctly configured in the frontend.

### "CORS error"

CORS issues usually occur in development when the frontend and backend are on different origins. Make sure the backend CORS settings include the frontend origin.

### "SQLAlchemy error: No such table"

Database tables may not be created. Run migrations:
```bash
docker-compose exec backend alembic upgrade head
```

## Getting Additional Help

If you encounter issues not covered in this guide:

1. Check the logs for detailed error messages
2. Review related documentation in the project
3. Create an issue in the project repository with details about the problem