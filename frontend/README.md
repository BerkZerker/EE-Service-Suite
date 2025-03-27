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
│   │   └── ui/           # UI elements
│   ├── contexts/         # React context providers
│   ├── pages/            # Page components
│   ├── services/         # API services
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
- **UI Components**: Buttons, inputs, cards, modals
- **Page Components**: Dashboard, customers, tickets, etc.
- **Form Components**: Various form controls with validation

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