import time
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app import models
from app.core.security import get_password_hash
from app.tests.utils.utils import random_lower_string, random_email
from app.tests.utils.admin import create_random_admin
from app.tests.utils.organization import create_random_organization


client = TestClient(app)


def test_login_access_token(db: Session) -> None:
    """Test employee login."""
    # Create organization
    organization = create_random_organization(db)
    
    # Create employee
    email = random_email()
    password = random_lower_string()
    name = random_lower_string()
    employee = models.Employee(
        email=email,
        hashed_password=get_password_hash(password),
        name=name,
        type="personal",
        organizationId=organization.id,
        createdAt=int(time.time() * 1000),
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    
    # Login
    login_data = {
        "username": email,
        "password": password,
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    
    # Check response
    assert response.status_code == 200
    content = response.json()
    assert "access_token" in content
    assert content["token_type"] == "bearer"


def test_login_admin_access_token(db: Session) -> None:
    """Test admin login."""
    # Create organization
    organization = create_random_organization(db)
    
    # Create admin
    email = random_email()
    password = random_lower_string()
    name = random_lower_string()
    admin = models.Admin(
        email=email,
        hashed_password=get_password_hash(password),
        name=name,
        organizationId=organization.id,
        createdAt=int(time.time() * 1000),
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    # Login
    login_data = {
        "username": email,
        "password": password,
    }
    response = client.post("/api/v1/auth/admin/login", data=login_data)
    
    # Check response
    assert response.status_code == 200
    content = response.json()
    assert "access_token" in content
    assert content["token_type"] == "bearer"


def test_generate_admin_api_key(db: Session) -> None:
    """Test generating an API key for admin."""
    # Create organization
    organization = create_random_organization(db)
    
    # Create admin
    email = random_email()
    password = random_lower_string()
    name = random_lower_string()
    admin = models.Admin(
        email=email,
        hashed_password=get_password_hash(password),
        name=name,
        organizationId=organization.id,
        createdAt=int(time.time() * 1000),
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    # Generate API key
    login_data = {
        "username": email,
        "password": password,
    }
    response = client.post("/api/v1/auth/admin/api-key", data=login_data)
    
    # Check response
    assert response.status_code == 200
    content = response.json()
    assert content["email"] == email
    assert content["name"] == name
    assert content["organizationId"] == organization.id
    assert content["id"] == admin.id
    assert "api_key" in content
    
    # Check database
    db.refresh(admin)
    assert admin.api_key == content["api_key"]