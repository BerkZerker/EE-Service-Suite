# CLAUDE.md - Agentic Coding Guidelines

## Commands
- **Setup**: `npm install` (frontend), `pip install -r requirements.txt` (backend)
- **Frontend Dev**: `npm run dev` (Vite)
- **Backend Dev**: `uvicorn main:app --reload`
- **Tests**: `pytest` (backend), `npm test` (frontend)
- **Single Test**: `pytest path/to/test.py::test_function -v`
- **Linting**: `flake8` (backend), `npm run lint` (frontend)
- **Type Check**: `mypy .` (backend), `npm run typecheck` (frontend)
- **Database Migration**: `alembic upgrade head` (backend)

## Code Style Guidelines
- **Frontend**: React 18 with functional components and hooks
- **Backend**: FastAPI with Pydantic schemas and SQLAlchemy ORM
- **Imports**: Group standard library, third-party, then local imports
- **Naming**: camelCase for JS/TS, snake_case for Python
- **Types**: Use TypeScript for frontend, Python type hints for backend
- **Error Handling**: Use try/except with specific exceptions in Python, try/catch in JS
- **API**: RESTful endpoints following FastAPI conventions
- **Database**: SQLite for development with SQLAlchemy models
- **Authentication**: JWT token-based authentication
- **Component Structure**: Layout, Page, and Reusable UI components
- **State Management**: React Context API + hooks

## Project Progress
- **Phase 1**: ✅ Project Setup & Foundation
- **Phase 2**: 🔄 Database & Backend Core
  - Completed:
    - Database schema design
    - Database migrations
    - Authentication system
    - Middleware setup
  - Next steps:
    - CRUD API endpoints
    - Error handling
    - API documentation
- **Phase 3**: 📅 Frontend Foundation