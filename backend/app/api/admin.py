import time
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth.dependencies import get_admin_user
from app.core.security import get_password_hash
from app.db.database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Admin)
def create_admin(
    admin_in: schemas.AdminCreate,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(get_admin_user),
) -> Any:
    """
    Create new admin.
    """
    admin = db.query(models.Admin).filter(models.Admin.email == admin_in.email).first()
    if admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin with this email already exists",
        )
    
    admin_data = admin_in.dict()
    hashed_password = get_password_hash(admin_data.pop("password"))
    
    db_admin = models.Admin(
        **admin_data,
        hashed_password=hashed_password,
        createdAt=int(time.time() * 1000)
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


@router.get("/", response_model=List[schemas.Admin])
def read_admins(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_admin: models.Admin = Depends(get_admin_user),
) -> Any:
    """
    Retrieve admins.
    """
    admins = db.query(models.Admin).filter(
        models.Admin.organizationId == current_admin.organizationId
    ).offset(skip).limit(limit).all()
    return admins


@router.get("/{admin_id}", response_model=schemas.Admin)
def read_admin(
    admin_id: str,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(get_admin_user),
) -> Any:
    """
    Get admin by ID.
    """
    admin = db.query(models.Admin).filter(models.Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found",
        )
    
    # Check if admin belongs to the same organization
    if admin.organizationId != current_admin.organizationId:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this admin",
        )
    
    return admin


@router.put("/{admin_id}", response_model=schemas.Admin)
def update_admin(
    admin_id: str,
    admin_in: schemas.AdminUpdate,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(get_admin_user),
) -> Any:
    """
    Update admin.
    """
    admin = db.query(models.Admin).filter(models.Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found",
        )
    
    # Check if admin belongs to the same organization
    if admin.organizationId != current_admin.organizationId:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this admin",
        )
    
    update_data = admin_in.dict(exclude_unset=True)
    
    if "password" in update_data:
        hashed_password = get_password_hash(update_data.pop("password"))
        update_data["hashed_password"] = hashed_password
    
    for field, value in update_data.items():
        setattr(admin, field, value)
    
    db.commit()
    db.refresh(admin)
    return admin


@router.delete("/{admin_id}", response_model=schemas.Admin)
def delete_admin(
    admin_id: str,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(get_admin_user),
) -> Any:
    """
    Delete admin.
    """
    admin = db.query(models.Admin).filter(models.Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found",
        )
    
    # Check if admin belongs to the same organization
    if admin.organizationId != current_admin.organizationId:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this admin",
        )
    
    # Prevent deleting yourself
    if admin.id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete yourself",
        )
    
    db.delete(admin)
    db.commit()
    return admin