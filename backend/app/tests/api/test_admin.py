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


def test_create_admin(db: Session) -> None:
    """Test creating an admin."""
    # Create organization and admin
    organization = create_random_organization(db)
    admin = create_random_admin(db, organization_id=organization.id)
    
    # Create access token for admin
    access_token = create_access_token(admin.id)
    
    # Admin data
    email = random_email()
    password = random_lower_string()
    name = random_lower_string()
    
    # Create admin
    response = client.post(
        "/api/v1/admin/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "email": email,
            "password": password,
            "name": name,
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
    new_admin = db.query(models.Admin).filter(models.Admin.email == email).first()
    assert new_admin is not None
    assert new_admin.email == email
    assert new_admin.name == name
    assert new_admin.organizationId == organization.id


def test_read_admins(db: Session) -> None:
    """Test reading admins."""
    # Create organization and admin
    organization = create_random_organization(db)
    admin = create_random_admin(db, organization_id=organization.id)
    
    # Create access token for admin
    access_token = create_access_token(admin.id)
    
    # Read admins
    response = client.get(
        "/api/v1/admin/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    
    # Check response
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 1
    assert content[0]["id"] == admin.id
    assert content[0]["email"] == admin.email
    assert content[0]["name"] == admin.name
    assert content[0]["organizationId"] == organization.id


def test_read_admin(db: Session) -> None:
    """Test reading an admin."""
    # Create organization and admin
    organization = create_random_organization(db)
    admin = create_random_admin(db, organization_id=organization.id)
    
    # Create access token for admin
    access_token = create_access_token(admin.id)
    
    # Read admin
    response = client.get(
        f"/api/v1/admin/{admin.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    
    # Check response
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == admin.id
    assert content["email"] == admin.email
    assert content["name"] == admin.name
    assert content["organizationId"] == organization.id


def test_update_admin(db: Session) -> None:
    """Test updating an admin."""
    # Create organization and admin
    organization = create_random_organization(db)
    admin = create_random_admin(db, organization_id=organization.id)
    
    # Create access token for admin
    access_token = create_access_token(admin.id)
    
    # Update admin
    new_name = random_lower_string()
    response = client.put(
        f"/api/v1/admin/{admin.id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"name": new_name},
    )
    
    # Check response
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == admin.id
    assert content["email"] == admin.email
    assert content["name"] == new_name
    assert content["organizationId"] == organization.id
    
    # Check database
    db.refresh(admin)
    assert admin.name == new_name


def test_delete_admin(db: Session) -> None:
    """Test deleting an admin."""
    # Create organization and two admins
    organization = create_random_organization(db)
    admin1 = create_random_admin(db, organization_id=organization.id)
    admin2 = create_random_admin(db, organization_id=organization.id)
    
    # Create access token for admin1
    access_token = create_access_token(admin1.id)
    
    # Delete admin2
    response = client.delete(
        f"/api/v1/admin/{admin2.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    
    # Check response
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == admin2.id
    assert content["email"] == admin2.email
    assert content["name"] == admin2.name
    assert content["organizationId"] == organization.id
    
    # Check database
    admin = db.query(models.Admin).filter(models.Admin.id == admin2.id).first()
    assert admin is None