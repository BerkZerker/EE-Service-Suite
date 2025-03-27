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

This project is currently in active development. We have completed Phase 1 setup tasks and Phase 2 backend development, and are now well into Phase 3 frontend development.

### Backend Progress (Phase 2: Complete ✅)
- ✅ Users CRUD API: Complete with authentication, role-based permissions, and comprehensive test coverage
- ✅ Customers CRUD API: Complete with search functionality, filtering, and relationship with bikes
- ✅ Bikes CRUD API: Complete with full lifecycle management, filtering by owner, and relationship with tickets
- ✅ Tickets CRUD API: Complete with updates, status tracking, and parts management
- ✅ Parts CRUD API: Complete with inventory management, stock adjustments, and low stock alerts
- ✅ Authentication system: JWT-based with refresh token mechanism
- ✅ API documentation: Swagger/ReDoc auto-generation for all endpoints

### Frontend Progress (Phase 3: In Progress 🔄)
- ✅ Authentication infrastructure: Context provider, protected routes, login page
- ✅ API service layer: Centralized API client with token refresh and error handling
- ✅ UI component library: Basic components (Button, Card, Input, Spinner) with Tailwind styling
- ✅ Layout and navigation: Responsive design with mobile support and dark theme
- 🔄 Customer management screens: In progress
- 🔄 Ticket listing and details: In progress

### Next Steps
- Complete form components for data entry
- Build customer management interfaces
- Develop ticket management screens
- Implement inventory tracking UI

## Getting Started

For setup and installation instructions, please refer to [SETUP.md](SETUP.md).

## Testing

### Test Account

For testing the application, use the following credentials:
- **Email**: admin@example.com
- **Password**: adminpassword

## License

This project is proprietary software developed for EE Service Suite.