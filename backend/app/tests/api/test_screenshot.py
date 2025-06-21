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


def test_create_screenshot(db: Session) -> None:
    """Test creating a screenshot."""
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
    
    # Screenshot data
    timestamp = int(time.time() * 1000)
    
    # Create screenshot
    response = client.post(
        "/api/v1/analytics/screenshot/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "employeeId": employee.id,
            "shiftId": shift.id,
            "timestamp": timestamp,
            "organizationId": organization.id,
            "projectId": project.id,
            "app": "Chrome",
            "title": "Test Page",
            "url": "https://example.com",
            "active": True,
        },
    )
    
    # Check response
    assert response.status_code == 200
    content = response.json()
    assert content["employeeId"] == employee.id
    assert content["shiftId"] == shift.id
    assert content["timestamp"] == timestamp
    assert content["organizationId"] == organization.id
    assert content["projectId"] == project.id
    assert content["app"] == "Chrome"
    assert content["title"] == "Test Page"
    assert content["url"] == "https://example.com"
    assert content["active"] is True
    assert "id" in content
    
    # Check database
    screenshot = db.query(models.Screenshot).filter(models.Screenshot.id == content["id"]).first()
    assert screenshot is not None
    assert screenshot.employeeId == employee.id
    assert screenshot.shiftId == shift.id
    assert screenshot.timestamp == timestamp
    assert screenshot.organizationId == organization.id
    assert screenshot.projectId == project.id
    assert screenshot.app == "Chrome"
    assert screenshot.title == "Test Page"
    assert screenshot.url == "https://example.com"
    assert screenshot.active is True


def test_read_screenshots(db: Session) -> None:
    """Test reading screenshots."""
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
    
    # Create shift
    start_time = int(time.time() * 1000) - 3600000  # 1 hour ago
    timezone_offset = -18000000  # -5 hours in milliseconds
    shift = models.Shift(
        type="manual",
        start=start_time,
        timezoneOffset=timezone_offset,
        employeeId=employee.id,
        organizationId=organization.id,
    )
    db.add(shift)
    db.commit()
    db.refresh(shift)
    
    # Create screenshots
    timestamp1 = int(time.time() * 1000) - 1800000  # 30 minutes ago
    timestamp2 = int(time.time() * 1000) - 900000   # 15 minutes ago
    
    screenshot1 = models.Screenshot(
        employeeId=employee.id,
        shiftId=shift.id,
        timestamp=timestamp1,
        organizationId=organization.id,
        app="Chrome",
        title="Test Page 1",
        url="https://example.com/1",
        active=True,
    )
    
    screenshot2 = models.Screenshot(
        employeeId=employee.id,
        shiftId=shift.id,
        timestamp=timestamp2,
        organizationId=organization.id,
        app="Firefox",
        title="Test Page 2",
        url="https://example.com/2",
        active=True,
    )
    
    db.add(screenshot1)
    db.add(screenshot2)
    db.commit()
    db.refresh(screenshot1)
    db.refresh(screenshot2)
    
    # Read screenshots
    response = client.get(
        f"/api/v1/analytics/screenshot/?start={timestamp1 - 3600000}&end={timestamp2 + 3600000}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    
    # Check response
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 2
    assert content[0]["id"] == screenshot1.id
    assert content[1]["id"] == screenshot2.id


def test_delete_screenshot(db: Session) -> None:
    """Test deleting a screenshot."""
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
    
    # Create shift
    start_time = int(time.time() * 1000) - 3600000  # 1 hour ago
    timezone_offset = -18000000  # -5 hours in milliseconds
    shift = models.Shift(
        type="manual",
        start=start_time,
        timezoneOffset=timezone_offset,
        employeeId=employee.id,
        organizationId=organization.id,
    )
    db.add(shift)
    db.commit()
    db.refresh(shift)
    
    # Create screenshot
    timestamp = int(time.time() * 1000) - 1800000  # 30 minutes ago
    
    screenshot = models.Screenshot(
        employeeId=employee.id,
        shiftId=shift.id,
        timestamp=timestamp,
        organizationId=organization.id,
        app="Chrome",
        title="Test Page",
        url="https://example.com",
        active=True,
    )
    
    db.add(screenshot)
    db.commit()
    db.refresh(screenshot)
    
    # Delete screenshot
    response = client.delete(
        f"/api/v1/analytics/screenshot/{screenshot.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    
    # Check response
    assert response.status_code == 204
    
    # Check database
    screenshot = db.query(models.Screenshot).filter(models.Screenshot.id == screenshot.id).first()
    assert screenshot is None
    
    # Check shift's deletedScreenshots counter
    db.refresh(shift)
    assert shift.deletedScreenshots == 1


def test_paginate_screenshots(db: Session) -> None:
    """Test paginating screenshots."""
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
    
    # Create shift
    start_time = int(time.time() * 1000) - 3600000  # 1 hour ago
    timezone_offset = -18000000  # -5 hours in milliseconds
    shift = models.Shift(
        type="manual",
        start=start_time,
        timezoneOffset=timezone_offset,
        employeeId=employee.id,
        organizationId=organization.id,
    )
    db.add(shift)
    db.commit()
    db.refresh(shift)
    
    # Create screenshots
    timestamp1 = int(time.time() * 1000) - 1800000  # 30 minutes ago
    timestamp2 = int(time.time() * 1000) - 1500000  # 25 minutes ago
    timestamp3 = int(time.time() * 1000) - 1200000  # 20 minutes ago
    
    screenshot1 = models.Screenshot(
        employeeId=employee.id,
        shiftId=shift.id,
        timestamp=timestamp1,
        organizationId=organization.id,
        app="Chrome",
        title="Test Page 1",
        url="https://example.com/1",
        active=True,
    )
    
    screenshot2 = models.Screenshot(
        employeeId=employee.id,
        shiftId=shift.id,
        timestamp=timestamp2,
        organizationId=organization.id,
        app="Firefox",
        title="Test Page 2",
        url="https://example.com/2",
        active=True,
    )
    
    screenshot3 = models.Screenshot(
        employeeId=employee.id,
        shiftId=shift.id,
        timestamp=timestamp3,
        organizationId=organization.id,
        app="Safari",
        title="Test Page 3",
        url="https://example.com/3",
        active=True,
    )
    
    db.add(screenshot1)
    db.add(screenshot2)
    db.add(screenshot3)
    db.commit()
    db.refresh(screenshot1)
    db.refresh(screenshot2)
    db.refresh(screenshot3)
    
    # Paginate screenshots (first page, limit 2)
    response = client.get(
        f"/api/v1/analytics/screenshot/paginate?start={timestamp1 - 3600000}&end={timestamp3 + 3600000}&limit=2",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    
    # Check response
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) == 2
    assert content["data"][0]["id"] == screenshot1.id
    assert content["data"][1]["id"] == screenshot2.id
    assert content["next"] == str(timestamp2)
    
    # Paginate screenshots (second page)
    response = client.get(
        f"/api/v1/analytics/screenshot/paginate?start={timestamp1 - 3600000}&end={timestamp3 + 3600000}&limit=2&next={content['next']}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    
    # Check response
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) == 1
    assert content["data"][0]["id"] == screenshot3.id
    assert content["next"] is None