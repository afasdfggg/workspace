from fastapi import APIRouter

from app.api import admin, employee, project, task, time_tracking, screenshot, auth

api_router = APIRouter()

# Auth routes
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# Admin routes
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])

# Employee routes
api_router.include_router(employee.router, prefix="/employee", tags=["employee"])

# Project routes
api_router.include_router(project.router, prefix="/project", tags=["project"])

# Task routes
api_router.include_router(task.router, prefix="/task", tags=["task"])

# Time tracking routes
api_router.include_router(time_tracking.router, prefix="/time-tracking", tags=["time-tracking"])

# Screenshot routes
api_router.include_router(screenshot.router, prefix="/analytics/screenshot", tags=["screenshot"])