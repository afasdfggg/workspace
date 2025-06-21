import time
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app import models
from app.core.security import create_access_token, get_password_hash
from app.tests.utils.utils import random_lower_string, random_email
from app.tests.utils.admin import create_random_admin
from app.tests.utils.organization import create_random_organization


client = TestClient(app)


def test_create_shift(db: Session) -> None:
    """Test creating a shift."""
    # Create organization and admin
    organization = create_random_organization(db)
    admin = create_random_admin(db, organization_id=organization.id)
    
    # Create employee
    email = random_email()
    name = random_lower_string()
    employee = models.Employee(
        email=email,
        name=name,
        hashed_password=get_password_hash("password"),
        type="personal",
        organizationId=organization.id,
        createdAt=int(time.time() * 1000),
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    
    # Create access token for employee
    access_token = create_access_token(employee.id)
    
    # Create project
    project_name = random_lower_string()
    project = models.Project(
        name=project_name,
        billable=True,
        organizationId=organization.id,
        creatorId=admin.id,
        createdAt=1234567890,
        archived=False,
        statuses=["To do", "In progress", "Done"],
        priorities=["low", "medium", "high"],
        screenshotSettings={"screenshotEnabled": True},
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    
    # Add employee to project
    project.employees.append(employee)
    db.commit()
    
    # Create task
    task_name = random_lower_string()
    task = models.Task(
        name=task_name,
        projectId=project.id,
        status="To Do",
        priority="low",
        billable=True,
        organizationId=organization.id,
        creatorId=admin.id,
        createdAt=1234567890,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    
    # Add employee to task
    task.employees.append(employee)
    db.commit()
    
    # Shift data
    start_time = int(time.time() * 1000)
    timezone_offset = -18000000  # -5 hours in milliseconds
    
    # Create shift
    response = client.post(
        "/api/v1/time-tracking/shift",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "type": "manual",
            "start": start_time,
            "timezoneOffset": timezone_offset,
            "employeeId": employee.id,
            "organizationId": organization.id,
            "projectId": project.id,
            "taskId": task.id,
        },
    )
    
    # Check response
    assert response.status_code == 200
    content = response.json()
    assert content["type"] == "manual"
    assert content["start"] == start_time
    assert content["timezoneOffset"] == timezone_offset
    assert content["employeeId"] == employee.id
    assert content["organizationId"] == organization.id
    assert content["projectId"] == project.id
    assert content["taskId"] == task.id
    assert "id" in content
    
    # Check database
    shift = db.query(models.Shift).filter(models.Shift.id == content["id"]).first()
    assert shift is not None
    assert shift.type == "manual"
    assert shift.start == start_time
    assert shift.timezoneOffset == timezone_offset
    assert shift.employeeId == employee.id
    assert shift.organizationId == organization.id
    assert shift.projectId == project.id
    assert shift.taskId == task.id


def test_update_shift(db: Session) -> None:
    """Test updating a shift."""
    # Create organization and admin
    organization = create_random_organization(db)
    admin = create_random_admin(db, organization_id=organization.id)
    
    # Create employee
    email = random_email()
    name = random_lower_string()
    employee = models.Employee(
        email=email,
        name=name,
        hashed_password=get_password_hash("password"),
        type="personal",
        organizationId=organization.id,
        createdAt=int(time.time() * 1000),
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    
    # Create access token for employee
    access_token = create_access_token(employee.id)
    
    # Create project
    project_name = random_lower_string()
    project = models.Project(
        name=project_name,
        billable=True,
        organizationId=organization.id,
        creatorId=admin.id,
        createdAt=1234567890,
        archived=False,
        statuses=["To do", "In progress", "Done"],
        priorities=["low", "medium", "high"],
        screenshotSettings={"screenshotEnabled": True},
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    
    # Add employee to project
    project.employees.append(employee)
    db.commit()
    
    # Create shift
    start_time = int(time.time() * 1000) - 3600000  # 1 hour ago
    timezone_offset = -18000000  # -5 hours in milliseconds
    shift = models.Shift(
        type="manual",
        start=start_time,
        timezoneOffset=timezone_offset,
        employeeId=employee.id,
        organizationId=organization.id,
        projectId=project.id,
    )
    db.add(shift)
    db.commit()
    db.refresh(shift)
    
    # Update shift (end time)
    end_time = int(time.time() * 1000)
    response = client.put(
        f"/api/v1/time-tracking/shift/{shift.id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"end": end_time},
    )
    
    # Check response
    assert response.status_code == 200
    content = response.json()
    assert content["type"] == "manual"
    assert content["start"] == start_time
    assert content["end"] == end_time
    assert content["timezoneOffset"] == timezone_offset
    assert content["employeeId"] == employee.id
    assert content["organizationId"] == organization.id
    assert content["projectId"] == project.id
    assert content["id"] == shift.id
    
    # Check database
    db.refresh(shift)
    assert shift.end == end_time


def test_get_project_time(db: Session) -> None:
    """Test getting project time analytics."""
    # Create organization and admin
    organization = create_random_organization(db)
    admin = create_random_admin(db, organization_id=organization.id)
    
    # Create access token for admin
    access_token = create_access_token(admin.id)
    
    # Create employee
    email = random_email()
    name = random_lower_string()
    employee = models.Employee(
        email=email,
        name=name,
        type="personal",
        organizationId=organization.id,
        createdAt=int(time.time() * 1000),
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    
    # Create project
    project_name = random_lower_string()
    project = models.Project(
        name=project_name,
        billable=True,
        organizationId=organization.id,
        creatorId=admin.id,
        createdAt=1234567890,
        archived=False,
        statuses=["To do", "In progress", "Done"],
        priorities=["low", "medium", "high"],
        screenshotSettings={"screenshotEnabled": True},
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    
    # Create task
    task_name = random_lower_string()
    task = models.Task(
        name=task_name,
        projectId=project.id,
        status="To Do",
        priority="low",
        billable=True,
        organizationId=organization.id,
        creatorId=admin.id,
        createdAt=1234567890,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    
    # Create shift
    start_time = int(time.time() * 1000) - 3600000  # 1 hour ago
    end_time = int(time.time() * 1000)
    timezone_offset = -18000000  # -5 hours in milliseconds
    shift = models.Shift(
        type="manual",
        start=start_time,
        end=end_time,
        timezoneOffset=timezone_offset,
        employeeId=employee.id,
        organizationId=organization.id,
        projectId=project.id,
        taskId=task.id,
    )
    db.add(shift)
    db.commit()
    db.refresh(shift)
    
    # Get project time
    response = client.get(
        f"/api/v1/time-tracking/analytics/project-time?start={start_time - 86400000}&end={end_time + 86400000}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    
    # Check response
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 1
    assert content[0]["projectId"] == project.id
    assert content[0]["projectName"] == project_name
    assert content[0]["taskId"] == task.id
    assert content[0]["taskName"] == task_name
    assert content[0]["employeeId"] == employee.id
    assert content[0]["employeeName"] == name
    assert content[0]["time"] == end_time - start_time
    assert content[0]["date"] == start_time