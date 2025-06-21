import time
from typing import Optional

from sqlalchemy.orm import Session

from app import models
from app.core.security import get_password_hash
from app.tests.utils.utils import random_email, random_lower_string


def create_random_admin(db: Session, organization_id: str) -> models.Admin:
    """Create a random admin for testing."""
    email = random_email()
    password = random_lower_string()
    name = random_lower_string()
    
    admin = models.Admin(
        email=email,
        hashed_password=get_password_hash(password),
        name=name,
        organizationId=organization_id,
        createdAt=int(time.time() * 1000),
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin