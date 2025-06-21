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


def test_create_project(db: Session) -> None:
    """Test creating a project."""
    # Create organization and admin
    organization = create_random_organization(db)
    admin = create_random_admin(db, organization_id=organization.id)
    
    # Create access token for admin
    access_token = create_access_token(admin.id)
    
    # Project data
    name = random_lower_string()
    description = random_lower_string()
    
    # Create project
    response = client.post(
        "/api/v1/project/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "name": name,
            "description": description,
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
    assert content["billable"] is True
    assert content["organizationId"] == organization.id
    assert content["creatorId"] == admin.id
    assert "id" in content
    
    # Check database
    project = db.query(models.Project).filter(models.Project.name == name).first()
    assert project is not None
    assert project.name == name
    assert project.description == description
    assert project.billable is True
    assert project.organizationId == organization.id
    assert project.creatorId == admin.id


def test_read_project(db: Session) -> None:
    """Test reading a project."""
    # Create organization and admin
    organization = create_random_organization(db)
    admin = create_random_admin(db, organization_id=organization.id)
    
    # Create access token for admin
    access_token = create_access_token(admin.id)
    
    # Create project
    name = random_lower_string()
    description = random_lower_string()
    project = models.Project(
        name=name,
        description=description,
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
    
    # Read project
    response = client.get(
        f"/api/v1/project/{project.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    
    # Check response
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == name
    assert content["description"] == description
    assert content["billable"] is True
    assert content["organizationId"] == organization.id
    assert content["creatorId"] == admin.id
    assert content["id"] == project.id


def test_update_project(db: Session) -> None:
    """Test updating a project."""
    # Create organization and admin
    organization = create_random_organization(db)
    admin = create_random_admin(db, organization_id=organization.id)
    
    # Create access token for admin
    access_token = create_access_token(admin.id)
    
    # Create project
    name = random_lower_string()
    description = random_lower_string()
    project = models.Project(
        name=name,
        description=description,
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
    
    # Update project
    new_name = random_lower_string()
    response = client.put(
        f"/api/v1/project/{project.id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"name": new_name},
    )
    
    # Check response
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == new_name
    assert content["description"] == description
    assert content["billable"] is True
    assert content["organizationId"] == organization.id
    assert content["creatorId"] == admin.id
    assert content["id"] == project.id
    
    # Check database
    db.refresh(project)
    assert project.name == new_name


def test_delete_project(db: Session) -> None:
    """Test deleting a project."""
    # Create organization and admin
    organization = create_random_organization(db)
    admin = create_random_admin(db, organization_id=organization.id)
    
    # Create access token for admin
    access_token = create_access_token(admin.id)
    
    # Create project
    name = random_lower_string()
    description = random_lower_string()
    project = models.Project(
        name=name,
        description=description,
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
    
    # Delete project
    response = client.delete(
        f"/api/v1/project/{project.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    
    # Check response
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == name
    assert content["description"] == description
    assert content["id"] == project.id
    
    # Check database
    project = db.query(models.Project).filter(models.Project.id == project.id).first()
    assert project is None