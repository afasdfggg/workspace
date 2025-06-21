import time
from typing import Optional

from sqlalchemy.orm import Session

from app import models
from app.tests.utils.utils import random_lower_string


def create_random_organization(db: Session) -> models.Organization:
    """Create a random organization for testing."""
    name = random_lower_string()
    
    organization = models.Organization(
        name=name,
        createdAt=int(time.time() * 1000),
    )
    db.add(organization)
    db.commit()
    db.refresh(organization)
    return organization