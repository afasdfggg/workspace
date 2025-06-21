# Insightful - Employee Time Tracking System

A comprehensive time tracking system for remote workers, consisting of a FastAPI backend, a Vue.js web application, and an Electron desktop client.

## Project Structure

- `backend`: FastAPI backend API
- `client/web`: Vue.js web application
- `client/electron`: Electron desktop client

## Features

- Employee management
- Project and task management
- Time tracking
- Screenshot capture
- Activity monitoring
- Role-based access control
- API key generation for admin users
- Email verification for new employees
- Password reset functionality

## Backend

The backend is built with FastAPI and provides a RESTful API for the web and desktop clients. It handles authentication, data storage, and business logic.

### Key Features

- JWT authentication
- Role-based access control
- Employee management
- Project and task management
- Time tracking
- Screenshot storage and retrieval
- Email notifications

### Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 12000
```

## Web Application

The web application is built with Vue.js and provides interfaces for both admin users and employees.

### Key Features

- Admin dashboard for managing employees, projects, tasks, and time tracking
- Employee dashboard for tracking time and viewing projects
- Authentication system with role-based access control
- API key generation for admin users
- Email verification for new employees
- Password reset functionality
- Responsive design for desktop and mobile devices

### Setup

```bash
cd client/web
npm install
npm run dev
```

## Desktop Client

The desktop client is built with Electron and provides a native application for employees to track time and capture screenshots.

### Key Features

- Time tracking
- Automatic screenshot capture
- Activity monitoring
- Offline support
- System tray integration

### Setup

```bash
cd client/electron
npm install
npm start
```

## Building for Production

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 12000
```

### Web Application

```bash
cd client/web
npm install
npm run build
```

### Desktop Client

```bash
cd client/electron
npm install
npm run dist
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.