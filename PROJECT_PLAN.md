# EE Service Suite
# PROJECT PLAN

## Project Overview

The EE Service Suite is a comprehensive web-based system designed to streamline the management of bike service operations. This locally-hosted application will enable staff to efficiently track service tickets, manage customer relationships, monitor inventory, and analyze business performance.

### Core V1 Focus
The initial version (V1) will prioritize:
1. **Service ticket tracking** - Complete workflow from intake to delivery
2. **Basic profit tracking** - Manual entry of parts costs and labor charges
3. **Simple inventory management** - Essential parts tracking with costs

Future versions will expand to include Shopify integration and advanced features while maintaining a foundation built for extensibility.

## Detailed Requirements

### 1. Ticket Management System
- **Create Service Tickets**
  - Customer information (name, contact, address)
  - Bike details (make, model, serial number, purchase date)
  - Accessories included
  - Problem description
  - Technician diagnosis
  - Parts required with costs
  - Labor charges
  - Auto-generated ticket number
  - Estimated completion date
  - Priority level (Low/Medium/High/Urgent)
  
- **Update Ticket Status**
  - Intake → Diagnosis → Awaiting Parts → In Progress → Complete → Delivered
  - Status change timestamps
  - Staff notes and updates

- **Ticket Archiving**
  - Archive completed tickets
  - Restore archived tickets when needed
  - View archive separately from active tickets

### 2. Search and Filter System
- Search by customer name, phone, ticket number, bike description
- Filter by:
  - Status
  - Date range (created/due)
  - Priority level
  - Technician assigned
  - Bike type

### 3. Customer Management
- Customer profiles with contact information
- Service history
- Multiple bikes per customer

### 4. Inventory Tracking
- Parts catalog with detailed specifications:
  - Part name, description, and categorization
  - Compatible bike makes/models
  - Manufacturer/supplier information
  - SKU/barcode for easy identification
- Comprehensive stock management:
  - Current quantity on hand
  - Minimum stock thresholds
  - Reorder points and preferred quantities
- Complete financial tracking:
  - Wholesale costs (purchase price)
  - Retail price and markup percentages
  - Cost history over time
- Parts usage tracking:
  - Automatic inventory deduction when used in service tickets
  - Usage history and trends
- Low stock alerts and notifications
- Purchase order creation and management

### 5. Financial Tracking
- Revenue per ticket
- Labor vs. parts breakdown
- Profit margins calculation
- Monthly/quarterly reports

### 6. User Management
- Staff accounts with login credentials
- Basic role-based permissions (Admin vs. Technician)

### 7. Data Backup
- Automated backups to Dropbox
- Manual backup option

## Technical Architecture

### Frontend Architecture
- **Framework**: React 18
- **State Management**: React Context API + hooks
- **Styling**: Tailwind CSS
- **Component Structure**:
  - Layout components (Header, Sidebar, Footer)
  - Page components (Dashboard, TicketList, TicketDetail, etc.)
  - Reusable UI components (Buttons, Forms, Modals, etc.)
- **Responsive Design**: Mobile-first approach with breakpoints

### Backend Architecture
- **Framework**: FastAPI (Python 3.9+)
- **API Structure**: RESTful endpoints
- **Authentication**: JWT token-based auth
- **Data Validation**: Pydantic schemas
- **ORM**: SQLAlchemy with async support
- **Database**: SQLite (with option to upgrade to PostgreSQL)
- **Future API Integration**:
  - Design with API integrations in mind (esp. Shopify)
  - Use adapter pattern to isolate external API dependencies
  - Implement data transformation services

### Database Schema
- **Users Table**: Staff account information
- **Customers Table**: Customer contact information
  - Include fields for future Shopify customer ID mapping
- **Bikes Table**: Bike specifications (related to customers)
- **Tickets Table**: Service ticket details
- **TicketUpdates Table**: Timeline of status changes and notes
- **Parts Table**: Inventory of parts
  - Part name, description, category
  - SKU/barcode
  - Compatibility data
  - Supplier information
  - Quantity on hand
  - Minimum stock threshold
  - Reorder point
  - Wholesale cost (purchase price)
  - Retail price and markup
  - Last ordered date
  - External ID field for future Shopify product mapping
- **TicketParts Table**: Junction table linking tickets to parts
  - Tracks which parts were used in which tickets
  - Records quantity used and price charged
- **Services Table**: Labor/service options with pricing

## Implementation Plan

### Phase 1: Project Setup & Foundation (Week 1)
- [x] Create GitHub repository structure
- [x] Set up development environment
- [x] Initialize backend project with FastAPI
- [x] Set up SQLAlchemy and database migrations
- [x] Initialize React frontend with Vite
- [x] Configure Tailwind CSS
- [x] Implement basic project structure
- [x] Create development Docker configuration
- [x] Implement Docker containerization
- [x] Initialize database with migrations

### Phase 2: Database & Backend Core (Weeks 2-3)
- [x] Design and implement database schema
- [x] Create database migrations
- [x] Implement user authentication system
- [x] Develop core API endpoints (priority order):
  - [x] Users CRUD (staff accounts)
  - [x] Customers CRUD (with automatic creation during ticket creation)
  - [x] Bikes CRUD (as subsection of customers)
  - [x] Tickets CRUD (with customer lookup/creation logic)
  - [x] Parts CRUD (with inventory management capabilities)
- [x] Implement authentication middleware
- [x] Set up error handling
- [x] Create API documentation with Swagger/ReDoc

### Phase 3: Frontend Foundation (Weeks 3-4)
- [x] Design component library and style guide
- [x] Implement layout components
- [x] Create authentication UI (Login, Password Reset)
- [x] Build navigation and routing
- [x] Implement dashboard view
- [x] Develop API service layer for frontend
- [x] Create form components for ticket creation/editing

### Phase 4: Ticket Management Features (Weeks 5-6)
- [x] Implement ticket creation flow
- [x] Build ticket detail view
- [x] Create ticket list with filtering capabilities
- [x] Implement status updates and history tracking
- [ ] Develop archiving and restoration functionality
- [x] Add customer lookup during ticket creation
- [x] Implement parts and services selection
- [x] Create parts management for tickets

### Phase 5: Search & Filtering System (Week 7)
- [ ] Develop advanced search functionality
- [ ] Implement filtering by multiple criteria
- [ ] Create saved searches/filters
- [ ] Build pagination for large result sets
- [ ] Implement sorting options

### Phase 6: Customer & Inventory Management (Week 8)
- [ ] Build customer profile page
- [ ] Implement service history view
- [ ] Create comprehensive inventory management system:
  - [ ] Parts catalog interface with detailed specifications
  - [ ] Stock level monitoring and management
  - [ ] Parts search and filtering
  - [ ] Compatibility lookups by bike make/model
- [ ] Develop parts usage tracking:
  - [ ] Automatic inventory deduction from tickets
  - [ ] Usage history and reporting
- [ ] Implement inventory alerts:
  - [ ] Low stock notifications
  - [ ] Reorder suggestions based on usage patterns
- [ ] Build purchase order system:
  - [ ] PO creation with supplier information
  - [ ] Cost tracking and order history
  - [ ] Receiving workflow to update inventory

### Phase 7: Analytics & Reporting (Week 9)
- [ ] Create financial dashboard:
  - [ ] Overall business performance metrics
  - [ ] Parts profit analysis (comparing wholesale vs. retail)
  - [ ] Inventory value reports
- [ ] Implement revenue reports:
  - [ ] Revenue breakdown by service type
  - [ ] Parts vs. labor contribution
  - [ ] Top-selling parts and services
- [ ] Develop profit margin calculations:
  - [ ] Ticket-level profitability
  - [ ] Per-part profit tracking
  - [ ] Overall margin trends over time
- [ ] Build technician productivity metrics
- [ ] Create exportable reports (PDF/CSV):
  - [ ] Inventory status reports
  - [ ] Parts usage history
  - [ ] Profit analysis

### Phase 8: Testing & Refinement (Week 10)
- [ ] Perform comprehensive testing
  - [ ] Unit tests for backend
  - [ ] Integration tests
  - [ ] UI testing
  - [ ] Responsive design testing
- [ ] Performance optimization
- [ ] Bug fixes and refinements
- [ ] Documentation updates

### Phase 9: Deployment & Backup (Week 11)
- [ ] Set up production environment on shop computer
- [ ] Configure production database
- [ ] Implement backup automation with Dropbox
- [ ] Create backup/restore procedures
- [ ] Deployment documentation

### Phase 10: Training & Handover (Week 12)
- [ ] Create user documentation
- [ ] Conduct staff training
- [ ] Collect initial feedback
- [ ] Make final adjustments
- [ ] Project handover

## Testing Strategy

### Backend Testing
- Unit tests for service layer logic
- API endpoint testing
- Database migration tests
- Authentication tests

### Frontend Testing
- Component tests with React Testing Library
- Form validation tests
- State management tests
- Responsive design tests

### Integration Testing
- End-to-end workflow tests
- API integration tests
- Authentication flow testing

## Deployment Strategy

### Docker Deployment (Recommended)
1. Install Docker and Docker Compose
2. Configure environment variables
3. Build and run containers
4. Initialize database
5. Configure network settings for local access
6. Set up automatic startup

### Alternative Local Deployment
1. Install required dependencies (Node.js, Python, SQLite)
2. Configure network settings for local access
3. Set up environment variables
4. Initialize database
5. Start backend and frontend services
6. Configure automatic startup

### Backup Strategy
1. SQLite database backup to local files
2. Automated Dropbox sync using official API
3. Schedule regular backups (daily)
4. Periodic backup verification

## Future Enhancements

### Potential Phase 11+ Features
- Shopify API integration:
  - Sync inventory data with online store
  - Import/export customer information
  - Update product availability based on stock levels
  - Streamline online order processing
- SMS notifications to customers
- Barcode/QR code scanning for quick ticket lookup
- Advanced inventory management with supplier integration
- Appointment scheduling system

## Risk Analysis

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Network reliability issues | Medium | High | Configure offline mode, local caching |
| Data loss | Low | Critical | Multiple backup strategies, transaction logging |
| System performance degradation | Medium | Medium | Database indexing, code optimization, monitoring |
| Security vulnerabilities | Low | High | Regular security updates, proper authentication |
| User adoption challenges | Medium | High | Intuitive UI, comprehensive training, feedback loop |