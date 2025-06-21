import time
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth.dependencies import get_admin_user, get_employee_user
from app.db.database import get_db

router = APIRouter()


@router.post("/shift", response_model=schemas.Shift)
def create_shift(
    shift_in: schemas.ShiftCreate,
    db: Session = Depends(get_db),
    current_user: models.Employee = Depends(get_employee_user),
) -> Any:
    """
    Create new shift (start time tracking).
    """
    # Ensure the employee is creating a shift for themselves
    if hasattr(current_user, 'api_key'):  # Admin
        employee = db.query(models.Employee).filter(models.Employee.id == shift_in.employeeId).first()
        if not employee or employee.organizationId != current_user.organizationId:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to create shift for this employee",
            )
    else:  # Employee
        if shift_in.employeeId != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot create shift for another employee",
            )
    
    # Check if project and task exist and are accessible
    if shift_in.projectId:
        project = db.query(models.Project).filter(models.Project.id == shift_in.projectId).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )
        
        # Check if employee has access to the project
        if not hasattr(current_user, 'api_key'):  # Employee
            if project not in current_user.projects:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions to track time for this project",
                )
    
    if shift_in.taskId:
        task = db.query(models.Task).filter(models.Task.id == shift_in.taskId).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
        
        # Check if employee has access to the task
        if not hasattr(current_user, 'api_key'):  # Employee
            if current_user not in task.employees:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions to track time for this task",
                )
    
    # Create shift
    db_shift = models.Shift(**shift_in.dict())
    db.add(db_shift)
    db.commit()
    db.refresh(db_shift)
    return db_shift


@router.put("/shift/{shift_id}", response_model=schemas.Shift)
def update_shift(
    shift_id: str,
    shift_in: schemas.ShiftUpdate,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_employee_user),
) -> Any:
    """
    Update shift (end time tracking or change project/task).
    """
    shift = db.query(models.Shift).filter(models.Shift.id == shift_id).first()
    if not shift:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shift not found",
        )
    
    # Check if user has access to the shift
    if hasattr(current_user, 'api_key'):  # Admin
        if shift.organizationId != current_user.organizationId:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to update this shift",
            )
    else:  # Employee
        if shift.employeeId != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot update shift for another employee",
            )
    
    # Check if project and task exist and are accessible
    if shift_in.projectId:
        project = db.query(models.Project).filter(models.Project.id == shift_in.projectId).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )
        
        # Check if employee has access to the project
        if not hasattr(current_user, 'api_key'):  # Employee
            if project not in current_user.projects:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions to track time for this project",
                )
    
    if shift_in.taskId:
        task = db.query(models.Task).filter(models.Task.id == shift_in.taskId).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
        
        # Check if employee has access to the task
        if not hasattr(current_user, 'api_key'):  # Employee
            if current_user not in task.employees:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions to track time for this task",
                )
    
    update_data = shift_in.dict(exclude_unset=True)
    
    # Update shift fields
    for field, value in update_data.items():
        setattr(shift, field, value)
    
    db.commit()
    db.refresh(shift)
    return shift


@router.get("/shift", response_model=List[schemas.Shift])
def read_shifts(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    employee_id: Optional[str] = None,
    project_id: Optional[str] = None,
    task_id: Optional[str] = None,
    current_user: Any = Depends(get_employee_user),
) -> Any:
    """
    Retrieve shifts.
    """
    query = db.query(models.Shift)
    
    # Filter by employee if specified
    if employee_id:
        query = query.filter(models.Shift.employeeId == employee_id)
    
    # Filter by project if specified
    if project_id:
        query = query.filter(models.Shift.projectId == project_id)
    
    # Filter by task if specified
    if task_id:
        query = query.filter(models.Shift.taskId == task_id)
    
    # If admin, return all shifts in the organization
    if hasattr(current_user, 'api_key'):
        query = query.filter(models.Shift.organizationId == current_user.organizationId)
    # If employee, return only their shifts
    else:
        query = query.filter(models.Shift.employeeId == current_user.id)
    
    shifts = query.offset(skip).limit(limit).all()
    return shifts


@router.get("/shift/{shift_id}", response_model=schemas.Shift)
def read_shift(
    shift_id: str,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_employee_user),
) -> Any:
    """
    Get shift by ID.
    """
    shift = db.query(models.Shift).filter(models.Shift.id == shift_id).first()
    if not shift:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shift not found",
        )
    
    # Check if user has access to the shift
    if hasattr(current_user, 'api_key'):  # Admin
        if shift.organizationId != current_user.organizationId:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to access this shift",
            )
    else:  # Employee
        if shift.employeeId != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot access shift for another employee",
            )
    
    return shift


@router.get("/analytics/project-time", response_model=List[schemas.ProjectTime])
def get_project_time(
    start: int = Query(..., description="Start time in milliseconds"),
    end: int = Query(..., description="End time in milliseconds"),
    timezone: Optional[str] = None,
    employee_id: Optional[str] = None,
    team_id: Optional[str] = None,
    project_id: Optional[str] = None,
    task_id: Optional[str] = None,
    shift_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_employee_user),
) -> Any:
    """
    Get project time analytics.
    """
    # Base query for shifts
    query = db.query(models.Shift).filter(
        models.Shift.start >= start,
        models.Shift.end <= end,
        models.Shift.end.isnot(None)  # Only include completed shifts
    )
    
    # Apply filters
    if employee_id:
        query = query.filter(models.Shift.employeeId == employee_id)
    
    if team_id:
        query = query.filter(models.Shift.teamId == team_id)
    
    if project_id:
        query = query.filter(models.Shift.projectId == project_id)
    
    if task_id:
        query = query.filter(models.Shift.taskId == task_id)
    
    if shift_id:
        query = query.filter(models.Shift.id == shift_id)
    
    # If admin, filter by organization
    if hasattr(current_user, 'api_key'):
        query = query.filter(models.Shift.organizationId == current_user.organizationId)
    # If employee, only show their shifts
    else:
        query = query.filter(models.Shift.employeeId == current_user.id)
    
    shifts = query.all()
    
    # Process shifts into project time data
    result = []
    for shift in shifts:
        if not shift.projectId:
            continue
        
        # Get project and task names
        project = db.query(models.Project).filter(models.Project.id == shift.projectId).first()
        task = None
        if shift.taskId:
            task = db.query(models.Task).filter(models.Task.id == shift.taskId).first()
        
        # Get employee name
        employee = db.query(models.Employee).filter(models.Employee.id == shift.employeeId).first()
        
        # Calculate time spent
        time_spent = shift.end - shift.start
        
        # Add to result
        result.append({
            "projectId": shift.projectId,
            "projectName": project.name if project else "Unknown Project",
            "taskId": shift.taskId,
            "taskName": task.name if task else None,
            "employeeId": shift.employeeId,
            "employeeName": employee.name if employee else "Unknown Employee",
            "time": time_spent,
            "date": shift.start
        })
    
    return result