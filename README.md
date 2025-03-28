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

This project is currently in active development. We have completed Phase 1 setup tasks, Phase 2 backend development, Phase 3 frontend foundation, and Phase 4 ticket management features. We're now preparing to implement Phase 5 with advanced search and filtering capabilities.

### Backend Progress (Phase 2: Complete ✅)
- ✅ Users CRUD API: Complete with authentication, role-based permissions, and comprehensive test coverage
- ✅ Customers CRUD API: Complete with search functionality, filtering, and relationship with bikes
- ✅ Bikes CRUD API: Complete with full lifecycle management, filtering by owner, and relationship with tickets
- ✅ Tickets CRUD API: Complete with updates, status tracking, and parts management
- ✅ Parts CRUD API: Complete with inventory management, stock adjustments, and low stock alerts
- ✅ Authentication system: JWT-based with refresh token mechanism
- ✅ API documentation: Swagger/ReDoc auto-generation for all endpoints

### Frontend Progress (Phase 3: Complete ✅)
- ✅ Authentication infrastructure: Context provider, protected routes, login page
- ✅ API service layer: Centralized API client with token refresh and error handling
- ✅ UI component library: Basic components with Tailwind styling (Buttons, Cards, Inputs, etc.)
- ✅ Layout and navigation: Responsive design with mobile support and dark theme
- ✅ Form components: Complete set of form controls for ticket creation and editing
- ✅ Dashboard view: Overview of system status and quick navigation

### Ticket Management (Phase 4: Complete ✅)
- ✅ Ticket creation flow: Form with customer selection, bike details, and parts
- ✅ Ticket listing page: Display tickets with status, priority, and filtering
- ✅ Customer lookup: Search and select customers during ticket creation
- ✅ Parts selection: Add parts to tickets with quantity and pricing
- ✅ Ticket detail view: View and manage all ticket information
- ✅ Status history tracking: Track and display ticket status changes with notes
- ✅ Parts management: Add, remove, and track parts used in tickets
- ✅ Archiving system: Complete with archive/unarchive functionality and visual indicators

### Next Steps
- Develop advanced search and filtering capabilities (Phase 5)
- Implement customer profile and service history views
- Create comprehensive inventory management dashboards
- Build analytics and reporting features

## Getting Started

For setup and installation instructions, please refer to [SETUP.md](SETUP.md).

## Testing

### Test Account

For testing the application, use the following credentials:
- **Email**: admin@example.com
- **Password**: adminpassword

## License

This project is proprietary software developed for EE Service Suite.