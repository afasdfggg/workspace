import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app import models
from app.core.security import create_access_token
from app.tests.utils.utils import random_email, random_lower_string
from app.tests.utils.admin import create_random_admin
from app.tests.utils.organization import create_random_organization


client = TestClient(app)


def test_create_employee(db: Session) -> None:
    """Test creating an employee."""
    # Create organization and admin
    organization = create_random_organization(db)
    admin = create_random_admin(db, organization_id=organization.id)
    
    # Create access token for admin
    access_token = create_access_token(admin.id)
    
    # Employee data
    email = random_email()
    name = random_lower_string()
    
    # Create employee
    response = client.post(
        "/api/v1/employee/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "name": name,
            "email": email,
            "type": "personal",
            "organizationId": organization.id,
        },
    )
    
    # Check response
    assert response.status_code == 200
    content = response.json()
    assert content["email"] == email
    assert content["name"] == name
    assert content["organizationId"] == organization.id
    assert "id" in content
    
    # Check database
    employee = db.query(models.Employee).filter(models.Employee.email == email).first()
    assert employee is not None
    assert employee.email == email
    assert employee.name == name
    assert employee.organizationId == organization.id


def test_read_employee(db: Session) -> None:
    """Test reading an employee."""
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
        createdAt=1234567890,
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    
    # Read employee
    response = client.get(
        f"/api/v1/employee/{employee.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    
    # Check response
    assert response.status_code == 200
    content = response.json()
    assert content["email"] == email
    assert content["name"] == name
    assert content["organizationId"] == organization.id
    assert content["id"] == employee.id


def test_update_employee(db: Session) -> None:
    """Test updating an employee."""
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
        createdAt=1234567890,
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    
    # Update employee
    new_name = random_lower_string()
    response = client.put(
        f"/api/v1/employee/{employee.id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"name": new_name},
    )
    
    # Check response
    assert response.status_code == 200
    content = response.json()
    assert content["email"] == email
    assert content["name"] == new_name
    assert content["organizationId"] == organization.id
    assert content["id"] == employee.id
    
    # Check database
    db.refresh(employee)
    assert employee.name == new_name


def test_deactivate_employee(db: Session) -> None:
    """Test deactivating an employee."""
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
        createdAt=1234567890,
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    
    # Deactivate employee
    response = client.put(
        f"/api/v1/employee/deactivate/{employee.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    
    # Check response
    assert response.status_code == 200
    content = response.json()
    assert content["email"] == email
    assert content["name"] == name
    assert content["organizationId"] == organization.id
    assert content["id"] == employee.id
    assert content["deactivated"] is not None
    
    # Check database
    db.refresh(employee)
    assert employee.deactivated is not None