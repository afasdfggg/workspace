import time
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth.dependencies import get_admin_user, get_employee_user, check_project_access
from app.db.database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Project)
def create_project(
    project_in: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(get_admin_user),
) -> Any:
    """
    Create new project.
    """
    # Ensure project belongs to the same organization as the admin
    if project_in.organizationId != current_admin.organizationId:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create project for different organization",
        )
    
    project_data = project_in.dict(exclude={"employees", "teams"})
    
    # Create project
    db_project = models.Project(
        **project_data,
        createdAt=int(time.time() * 1000)
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    # Add employees if specified
    if project_in.employees:
        for employee_id in project_in.employees:
            employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
            if employee and employee.organizationId == current_admin.organizationId:
                db_project.employees.append(employee)
    
    # Add teams if specified
    if project_in.teams:
        for team_id in project_in.teams:
            team = db.query(models.Team).filter(models.Team.id == team_id).first()
            if team and team.organizationId == current_admin.organizationId:
                db_project.teams.append(team)
    
    db.commit()
    db.refresh(db_project)
    return db_project


@router.get("/", response_model=List[schemas.Project])
def read_projects(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(get_employee_user),
) -> Any:
    """
    Retrieve projects.
    """
    # If admin, return all projects in the organization
    if hasattr(current_user, 'api_key'):
        projects = db.query(models.Project).filter(
            models.Project.organizationId == current_user.organizationId
        ).offset(skip).limit(limit).all()
    # If employee, return only projects they are assigned to
    else:
        projects = current_user.projects
    
    return projects


@router.get("/{project_id}", response_model=schemas.Project)
def read_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: Any = Depends(check_project_access),
) -> Any:
    """
    Get project by ID.
    """
    # The check_project_access dependency already validates access and returns the project
    return current_user


@router.put("/{project_id}", response_model=schemas.Project)
def update_project(
    project_id: str,
    project_in: schemas.ProjectUpdate,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(get_admin_user),
) -> Any:
    """
    Update project.
    """
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    # Check if project belongs to the same organization
    if project.organizationId != current_admin.organizationId:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this project",
        )
    
    update_data = project_in.dict(exclude_unset=True, exclude={"employees", "teams"})
    
    # Update project fields
    for field, value in update_data.items():
        setattr(project, field, value)
    
    # Update employees if specified
    if project_in.employees is not None:
        # Clear existing employees
        project.employees = []
        
        # Add new employees
        for employee_id in project_in.employees:
            employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
            if employee and employee.organizationId == current_admin.organizationId:
                project.employees.append(employee)
    
    # Update teams if specified
    if project_in.teams is not None:
        # Clear existing teams
        project.teams = []
        
        # Add new teams
        for team_id in project_in.teams:
            team = db.query(models.Team).filter(models.Team.id == team_id).first()
            if team and team.organizationId == current_admin.organizationId:
                project.teams.append(team)
    
    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}", response_model=schemas.Project)
def delete_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(get_admin_user),
) -> Any:
    """
    Delete project.
    """
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    # Check if project belongs to the same organization
    if project.organizationId != current_admin.organizationId:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this project",
        )
    
    # Delete associated tasks
    tasks = db.query(models.Task).filter(models.Task.projectId == project_id).all()
    for task in tasks:
        db.delete(task)
    
    db.delete(project)
    db.commit()
    return project