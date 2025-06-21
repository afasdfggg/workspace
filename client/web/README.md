# Insightful Web Application

A web application for the Insightful time tracking system.

## Features

- Admin dashboard for managing employees, projects, tasks, and time tracking
- Employee dashboard for tracking time and viewing projects
- Authentication system with role-based access control
- API key generation for admin users
- Email verification for new employees
- Password reset functionality
- Responsive design for desktop and mobile devices

## Installation

### Prerequisites

- Node.js 14+
- npm or yarn

### Setup

1. Clone the repository
2. Install dependencies:

```bash
cd client/web
npm install
```

3. Run the development server:

```bash
npm run dev
```

## Building for Production

To build the application for production:

```bash
npm run build
```

The built files will be in the `dist` directory.

## Project Structure

- `src/assets`: Static assets like images and styles
- `src/components`: Reusable Vue components
- `src/views`: Page components
- `src/router`: Vue Router configuration
- `src/store`: Vuex store modules
- `src/services`: API services
- `src/utils`: Utility functions

## Authentication

The application uses JWT for authentication. The token is stored in localStorage and included in the Authorization header for API requests.

## Role-Based Access Control

The application has two roles:
- Admin: Can manage employees, projects, tasks, and view all time tracking data
- Employee: Can track time, view assigned projects, and view their own time tracking data

## API Integration

The application integrates with the Insightful API. The API base URL can be configured in the `.env` file.

## License

This project is licensed under the MIT License - see the LICENSE file for details.