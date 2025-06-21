import time
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth.dependencies import get_admin_user, get_employee_user, check_employee_access
from app.core.security import get_password_hash
from app.db.database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Employee)
def create_employee(
    employee_in: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(get_admin_user),
) -> Any:
    """
    Create new employee.
    """
    employee = db.query(models.Employee).filter(models.Employee.email == employee_in.email).first()
    if employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee with this email already exists",
        )
    
    # Ensure employee belongs to the same organization as the admin
    if employee_in.organizationId != current_admin.organizationId:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create employee for different organization",
        )
    
    employee_data = employee_in.dict(exclude={"projects"})
    
    # Create employee
    db_employee = models.Employee(
        **employee_data,
        invited=int(time.time() * 1000),  # Set invitation time
        createdAt=int(time.time() * 1000)
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    
    # Add projects if specified
    if employee_in.projects:
        for project_id in employee_in.projects:
            project = db.query(models.Project).filter(models.Project.id == project_id).first()
            if project and project.organizationId == current_admin.organizationId:
                db_employee.projects.append(project)
        
        db.commit()
        db.refresh(db_employee)
    
    # TODO: Send email verification link to employee
    
    return db_employee


@router.get("/", response_model=List[schemas.Employee])
def read_employees(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_admin: models.Admin = Depends(get_admin_user),
) -> Any:
    """
    Retrieve employees.
    """
    employees = db.query(models.Employee).filter(
        models.Employee.organizationId == current_admin.organizationId
    ).offset(skip).limit(limit).all()
    return employees


@router.get("/{employee_id}", response_model=schemas.Employee)
def read_employee(
    employee_id: str,
    db: Session = Depends(get_db),
    current_user: Any = Depends(check_employee_access),
) -> Any:
    """
    Get employee by ID.
    """
    # The check_employee_access dependency already validates access and returns the employee
    return current_user


@router.put("/{employee_id}", response_model=schemas.Employee)
def update_employee(
    employee_id: str,
    employee_in: schemas.EmployeeUpdate,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(get_admin_user),
) -> Any:
    """
    Update employee.
    """
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    
    # Check if employee belongs to the same organization
    if employee.organizationId != current_admin.organizationId:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this employee",
        )
    
    update_data = employee_in.dict(exclude_unset=True, exclude={"projects"})
    
    # Update employee fields
    for field, value in update_data.items():
        setattr(employee, field, value)
    
    # Update projects if specified
    if employee_in.projects is not None:
        # Clear existing projects
        employee.projects = []
        
        # Add new projects
        for project_id in employee_in.projects:
            project = db.query(models.Project).filter(models.Project.id == project_id).first()
            if project and project.organizationId == current_admin.organizationId:
                employee.projects.append(project)
    
    db.commit()
    db.refresh(employee)
    return employee


@router.post("/{employee_id}/set-password", response_model=schemas.Employee)
def set_employee_password(
    employee_id: str,
    password_in: schemas.EmployeeSetPassword,
    db: Session = Depends(get_db),
    current_user: Any = Depends(check_employee_access),
) -> Any:
    """
    Set employee password.
    """
    # The check_employee_access dependency already validates access and returns the employee
    employee = current_user
    
    # Set password
    hashed_password = get_password_hash(password_in.password)
    employee.hashed_password = hashed_password
    
    db.commit()
    db.refresh(employee)
    return employee


@router.put("/deactivate/{employee_id}", response_model=schemas.Employee)
def deactivate_employee(
    employee_id: str,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(get_admin_user),
) -> Any:
    """
    Deactivate employee.
    """
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    
    # Check if employee belongs to the same organization
    if employee.organizationId != current_admin.organizationId:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to deactivate this employee",
        )
    
    # Check if employee is already deactivated
    if employee.deactivated:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee is already deactivated",
        )
    
    # Deactivate employee
    employee.deactivated = int(time.time() * 1000)
    
    db.commit()
    db.refresh(employee)
    return employee