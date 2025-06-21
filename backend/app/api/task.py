import time
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth.dependencies import get_admin_user, get_employee_user, check_task_access
from app.db.database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Task)
def create_task(
    task_in: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_employee_user),
) -> Any:
    """
    Create new task.
    """
    # Check if project exists and user has access to it
    project = db.query(models.Project).filter(models.Project.id == task_in.projectId).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    # Check if user has access to the project
    if hasattr(current_user, 'api_key'):  # Admin
        if project.organizationId != current_user.organizationId:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to create task in this project",
            )
        creator_id = current_user.id
    else:  # Employee
        if project not in current_user.projects:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to create task in this project",
            )
        creator_id = current_user.id
    
    task_data = task_in.dict(exclude={"employees", "teams"})
    task_data["creatorId"] = creator_id
    
    # Create task
    db_task = models.Task(
        **task_data,
        createdAt=int(time.time() * 1000)
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    # Add employees if specified
    if task_in.employees:
        for employee_id in task_in.employees:
            employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
            if employee and employee.organizationId == project.organizationId:
                db_task.employees.append(employee)
    
    # Add teams if specified
    if task_in.teams:
        for team_id in task_in.teams:
            team = db.query(models.Team).filter(models.Team.id == team_id).first()
            if team and team.organizationId == project.organizationId:
                db_task.teams.append(team)
    
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/", response_model=List[schemas.Task])
def read_tasks(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[str] = None,
    current_user: Any = Depends(get_employee_user),
) -> Any:
    """
    Retrieve tasks.
    """
    query = db.query(models.Task)
    
    # Filter by project if specified
    if project_id:
        query = query.filter(models.Task.projectId == project_id)
    
    # If admin, return all tasks in the organization
    if hasattr(current_user, 'api_key'):
        query = query.filter(models.Task.organizationId == current_user.organizationId)
    # If employee, return only tasks they are assigned to
    else:
        query = query.filter(models.Task.employees.any(models.Employee.id == current_user.id))
    
    tasks = query.offset(skip).limit(limit).all()
    return tasks


@router.get("/{task_id}", response_model=schemas.Task)
def read_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: Any = Depends(check_task_access),
) -> Any:
    """
    Get task by ID.
    """
    # The check_task_access dependency already validates access and returns the task
    return current_user


@router.put("/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: str,
    task_in: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_employee_user),
) -> Any:
    """
    Update task.
    """
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    # Check if user has access to the task
    if hasattr(current_user, 'api_key'):  # Admin
        if task.organizationId != current_user.organizationId:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to update this task",
            )
    else:  # Employee
        project = db.query(models.Project).filter(models.Project.id == task.projectId).first()
        if project not in current_user.projects and current_user not in task.employees:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to update this task",
            )
    
    update_data = task_in.dict(exclude_unset=True, exclude={"employees"})
    
    # Update task fields
    for field, value in update_data.items():
        setattr(task, field, value)
    
    # Update employees if specified
    if task_in.employees is not None:
        # Clear existing employees
        task.employees = []
        
        # Add new employees
        for employee_id in task_in.employees:
            employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
            if employee and employee.organizationId == task.organizationId:
                task.employees.append(employee)
    
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", response_model=schemas.Task)
def delete_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_employee_user),
) -> Any:
    """
    Delete task.
    """
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    # Check if user has access to the task
    if hasattr(current_user, 'api_key'):  # Admin
        if task.organizationId != current_user.organizationId:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to delete this task",
            )
    else:  # Employee
        # Only the creator can delete a task
        if task.creatorId != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to delete this task",
            )
    
    db.delete(task)
    db.commit()
    return task