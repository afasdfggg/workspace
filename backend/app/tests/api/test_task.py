import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app import models
from app.core.security import create_access_token
from app.tests.utils.utils import random_lower_string
from app.tests.utils.admin import create_random_admin
from app.tests.utils.organization import create_random_organization


client = TestClient(app)


def test_create_task(db: Session) -> None:
    """Test creating a task."""
    # Create organization and admin
    organization = create_random_organization(db)
    admin = create_random_admin(db, organization_id=organization.id)
    
    # Create access token for admin
    access_token = create_access_token(admin.id)
    
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
    
    # Task data
    name = random_lower_string()
    description = random_lower_string()
    
    # Create task
    response = client.post(
        "/api/v1/task/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "name": name,
            "description": description,
            "projectId": project.id,
            "status": "To Do",
            "priority": "low",
            "billable": True,
            "organizationId": organization.id,
            "creatorId": admin.id,
        },
    )
    
    # Check response
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == name
    assert content["description"] == description
    assert content["projectId"] == project.id
    assert content["status"] == "To Do"
    assert content["priority"] == "low"
    assert content["billable"] is True
    assert content["organizationId"] == organization.id
    assert content["creatorId"] == admin.id
    assert "id" in content
    
    # Check database
    task = db.query(models.Task).filter(models.Task.name == name).first()
    assert task is not None
    assert task.name == name
    assert task.description == description
    assert task.projectId == project.id
    assert task.status == "To Do"
    assert task.priority == "low"
    assert task.billable is True
    assert task.organizationId == organization.id
    assert task.creatorId == admin.id


def test_read_task(db: Session) -> None:
    """Test reading a task."""
    # Create organization and admin
    organization = create_random_organization(db)
    admin = create_random_admin(db, organization_id=organization.id)
    
    # Create access token for admin
    access_token = create_access_token(admin.id)
    
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
    name = random_lower_string()
    description = random_lower_string()
    task = models.Task(
        name=name,
        description=description,
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
    
    # Read task
    response = client.get(
        f"/api/v1/task/{task.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    
    # Check response
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == name
    assert content["description"] == description
    assert content["projectId"] == project.id
    assert content["status"] == "To Do"
    assert content["priority"] == "low"
    assert content["billable"] is True
    assert content["organizationId"] == organization.id
    assert content["creatorId"] == admin.id
    assert content["id"] == task.id


def test_update_task(db: Session) -> None:
    """Test updating a task."""
    # Create organization and admin
    organization = create_random_organization(db)
    admin = create_random_admin(db, organization_id=organization.id)
    
    # Create access token for admin
    access_token = create_access_token(admin.id)
    
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
    name = random_lower_string()
    description = random_lower_string()
    task = models.Task(
        name=name,
        description=description,
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
    
    # Update task
    new_name = random_lower_string()
    response = client.put(
        f"/api/v1/task/{task.id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"name": new_name},
    )
    
    # Check response
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == new_name
    assert content["description"] == description
    assert content["projectId"] == project.id
    assert content["status"] == "To Do"
    assert content["priority"] == "low"
    assert content["billable"] is True
    assert content["organizationId"] == organization.id
    assert content["creatorId"] == admin.id
    assert content["id"] == task.id
    
    # Check database
    db.refresh(task)
    assert task.name == new_name


def test_delete_task(db: Session) -> None:
    """Test deleting a task."""
    # Create organization and admin
    organization = create_random_organization(db)
    admin = create_random_admin(db, organization_id=organization.id)
    
    # Create access token for admin
    access_token = create_access_token(admin.id)
    
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
    name = random_lower_string()
    description = random_lower_string()
    task = models.Task(
        name=name,
        description=description,
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
    
    # Delete task
    response = client.delete(
        f"/api/v1/task/{task.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    
    # Check response
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == name
    assert content["description"] == description
    assert content["id"] == task.id
    
    # Check database
    task = db.query(models.Task).filter(models.Task.id == task.id).first()
    assert task is None