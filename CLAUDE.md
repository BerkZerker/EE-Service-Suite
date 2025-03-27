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
- **Docker**: `docker-compose up -d` (Start all services)
- **Docker Rebuild**: `docker-compose down && docker-compose up -d --build` (Rebuild and restart)

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

## Frontend Component Guidelines
- All components should be functional components with TypeScript typing
- Use interface for component props
- UI components should be in src/components/ui
- Feature-specific components should be in their own directories (e.g., tickets)
- Prefer explicit imports over barrel exports for better performance
- Forms should implement proper validation and error handling
- Use Tailwind for styling with consistent patterns
- Always handle loading, success, and error states

## Project Progress
- **Phase 1**: ✅ Project Setup & Foundation
- **Phase 2**: ✅ Database & Backend Core
  - Completed:
    - Database schema design
    - Database migrations
    - Authentication system
    - Middleware setup
    - CRUD API endpoints
    - Error handling
    - API documentation
- **Phase 3**: ✅ Frontend Foundation
  - Completed:
    - Authentication infrastructure
    - API service layer
    - UI component library (basic and form components)
    - Layout and navigation structure
    - Form components for ticket creation/editing
- **Phase 4**: 🔄 Ticket Management Features
  - Completed:
    - Ticket creation flow
    - Ticket listing with filters
    - Customer lookup and selection
    - Parts selection with pricing
  - Next steps:
    - Complete ticket detail view
    - Implement status history tracking
    - Build archiving functionality