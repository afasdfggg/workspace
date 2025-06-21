# Employee Tracking API

This is a FastAPI backend for an employee tracking system, compatible with the Insightful API.

## Features

- Employee management
- Project management
- Task management
- Time tracking
- Screenshot capture and management
- Admin dashboard
- User authentication and authorization
- API key generation for admins

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables (or use the provided .env file):

```
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./insightful.db
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```

### Running the Application

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## Testing

Run tests with pytest:

```bash
pytest app/tests
```

## API Endpoints

### Authentication

- `POST /api/v1/auth/login` - Employee login
- `POST /api/v1/auth/admin/login` - Admin login
- `POST /api/v1/auth/admin/api-key` - Generate API key for admin

### Admin Management

- `GET /api/v1/admin/` - List all admins
- `POST /api/v1/admin/` - Create a new admin
- `GET /api/v1/admin/{admin_id}` - Get admin details
- `PUT /api/v1/admin/{admin_id}` - Update admin
- `DELETE /api/v1/admin/{admin_id}` - Delete admin

### Employee Management

- `GET /api/v1/employee/` - List all employees
- `POST /api/v1/employee/` - Create a new employee
- `GET /api/v1/employee/{employee_id}` - Get employee details
- `PUT /api/v1/employee/{employee_id}` - Update employee
- `PUT /api/v1/employee/deactivate/{employee_id}` - Deactivate employee

### Project Management

- `GET /api/v1/project/` - List all projects
- `POST /api/v1/project/` - Create a new project
- `GET /api/v1/project/{project_id}` - Get project details
- `PUT /api/v1/project/{project_id}` - Update project
- `DELETE /api/v1/project/{project_id}` - Delete project

### Task Management

- `GET /api/v1/task/` - List all tasks
- `POST /api/v1/task/` - Create a new task
- `GET /api/v1/task/{task_id}` - Get task details
- `PUT /api/v1/task/{task_id}` - Update task
- `DELETE /api/v1/task/{task_id}` - Delete task

### Time Tracking

- `POST /api/v1/time-tracking/shift` - Create a new shift (start time tracking)
- `PUT /api/v1/time-tracking/shift/{shift_id}` - Update shift (end time tracking)
- `GET /api/v1/time-tracking/shift` - List shifts
- `GET /api/v1/time-tracking/shift/{shift_id}` - Get shift details
- `GET /api/v1/time-tracking/analytics/project-time` - Get project time analytics

### Screenshots

- `POST /api/v1/analytics/screenshot/` - Create a new screenshot
- `GET /api/v1/analytics/screenshot/` - List screenshots
- `DELETE /api/v1/analytics/screenshot/{screenshot_id}` - Delete screenshot
- `GET /api/v1/analytics/screenshot/paginate` - Paginate screenshots

## License

This project is licensed under the MIT License - see the LICENSE file for details.