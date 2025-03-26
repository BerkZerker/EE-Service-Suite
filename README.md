# EE Service Suite

A comprehensive web-based system for tracking and managing bicycle service operations.

## Overview

This application provides a complete solution for e-bike service management, enabling staff to track service tickets, manage customer relationships, monitor inventory, and analyze business performance. Built with a modern tech stack, it offers a responsive interface accessible from shop computers and mobile devices.

## Key Features

- **Service Ticket Management**: Create, update, and track service tickets with detailed information
- **Customer Database**: Store and manage customer profiles and service history
- **Inventory Tracking**: Monitor parts usage and stock levels
- **Financial Analysis**: Track revenue, costs, and profit margins
- **Search & Filtering**: Quickly find tickets by various criteria
- **User Management**: Role-based access control for staff
- **Local Hosting**: No dependence on external services
- **Automated Backups**: Secure data with Dropbox integration

## Tech Stack

- **Frontend**: React.js, Tailwind CSS, Vite
- **Backend**: FastAPI (Python), SQLAlchemy ORM
- **Database**: SQLite (upgradable to PostgreSQL)
- **Authentication**: JWT token-based auth
- **Deployment**: Docker and Docker Compose

## Development Status

This project is currently in active development. All Phase 1 setup tasks are complete, including Docker containerization and database initialization.

Progress so far:
- ✅ Users CRUD API: Complete with authentication, role-based permissions, and comprehensive test coverage
- ✅ Customers CRUD API: Complete with search functionality, filtering, and relationship with bikes
- 🔄 Tickets CRUD: Next up

Development is focusing on implementing the core API endpoints in the following priority order:
1. ✅ Users CRUD (staff accounts)
2. ✅ Customers CRUD (with search functionality and bikes integration)
3. 🔄 Tickets CRUD (with customer lookup/creation logic)
4. Bikes CRUD (as subsection of customers)
5. Parts CRUD (lowest priority)

See the [Project Plan](PROJECT_PLAN.md) for detailed implementation steps and timeline.

## Getting Started

For setup and installation instructions, please refer to [SETUP.md](SETUP.md).

## License

This project is proprietary software developed for EE Service Suite.