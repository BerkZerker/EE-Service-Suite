# EE Service Suite - Frontend

This is the frontend application for the EE Service Suite, built with React, TypeScript, and Tailwind CSS.

## Features

- **Modern React**: Built with React 18 and functional components
- **Type Safety**: Full TypeScript implementation
- **Styling**: Tailwind CSS for utility-first styling
- **State Management**: React Context API for global state
- **Form Handling**: React Hook Form with Zod validation
- **Routing**: React Router for navigation
- **API Integration**: Axios with interceptors for API communication

## Project Structure

```
frontend/
├── public/               # Static assets
├── src/                  # Source code
│   ├── components/       # Reusable UI components
│   │   ├── layout/       # Layout components
│   │   ├── ui/           # UI elements (Button, Input, etc.)
│   │   ├── auth/         # Authentication components
│   │   └── tickets/      # Ticket-specific components
│   ├── contexts/         # React context providers
│   ├── pages/            # Page components
│   │   ├── Dashboard.tsx     # Dashboard page
│   │   ├── Login.tsx         # Login page
│   │   ├── TicketList.tsx    # Ticket list page
│   │   ├── CreateTicket.tsx  # Ticket creation page
│   │   └── EditTicket.tsx    # Ticket editing page
│   ├── services/         # API services
│   │   ├── api-client.ts     # Base API client with interceptors
│   │   ├── auth-service.ts   # Authentication service
│   │   ├── ticket-service.ts # Ticket management service
│   │   └── part-service.ts   # Parts management service
│   ├── utils/            # Utility functions
│   ├── config/           # Configuration files
│   ├── App.tsx           # Main application component
│   └── main.tsx          # Application entry point
├── index.html            # HTML template
├── package.json          # Dependencies and scripts
└── tsconfig.json         # TypeScript configuration
```

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Build for production:
   ```bash
   npm run build
   ```

## Available Scripts

- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm run preview`: Preview production build
- `npm run lint`: Run ESLint
- `npm run typecheck`: Run TypeScript type checking
- `npm test`: Run tests

## Components

The frontend includes the following major component categories:

- **Layout Components**: Main layout, sidebar, header
- **UI Components**: 
  - Buttons, Inputs, Cards, Spinners
  - Select, TextArea, DatePicker, FormGroup, RadioGroup
- **Page Components**: 
  - Dashboard, Login, NotFound
  - Tickets (List, Create, Edit)
- **Form Components**:
  - TicketForm: Complete ticket creation/editing form
  - CustomerSelector: Search and select customers
  - BikeSelector: Choose customer bikes
  - PartsSelector: Add parts with quantities and pricing

## Authentication

The application uses JWT token authentication with:

- Protected routes to restrict access to authenticated users
- Token refresh functionality to maintain sessions
- User context for global auth state

## Testing Credentials

For testing the application, use:
- **Email:** admin@example.com
- **Password:** adminpassword

## Styling

The application uses Tailwind CSS with a custom configuration:

- Custom color palette for primary and secondary colors
- Dark mode by default
- Custom utility classes for common patterns
- Responsive design with mobile-first approach