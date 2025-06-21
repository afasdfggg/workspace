import time
import hashlib
import json
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth.dependencies import get_admin_user, get_employee_user
from app.db.database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Screenshot)
def create_screenshot(
    screenshot_in: schemas.ScreenshotCreate,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_employee_user),
) -> Any:
    """
    Create new screenshot.
    """
    # Ensure the screenshot is for the current user or admin has permission
    if hasattr(current_user, 'api_key'):  # Admin
        employee = db.query(models.Employee).filter(models.Employee.id == screenshot_in.employeeId).first()
        if not employee or employee.organizationId != current_user.organizationId:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to create screenshot for this employee",
            )
    else:  # Employee
        if screenshot_in.employeeId != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot create screenshot for another employee",
            )
    
    # Check if shift exists
    shift = db.query(models.Shift).filter(models.Shift.id == screenshot_in.shiftId).first()
    if not shift:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shift not found",
        )
    
    # Create screenshot
    db_screenshot = models.Screenshot(**screenshot_in.dict())
    db.add(db_screenshot)
    db.commit()
    db.refresh(db_screenshot)
    return db_screenshot


@router.get("/", response_model=List[schemas.Screenshot])
def read_screenshots(
    start: int = Query(..., description="Start time in milliseconds"),
    end: int = Query(..., description="End time in milliseconds"),
    limit: int = Query(15, description="Maximum number of screenshots to return"),
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_employee_user),
) -> Any:
    """
    Retrieve screenshots.
    """
    query = db.query(models.Screenshot).filter(
        models.Screenshot.timestamp >= start,
        models.Screenshot.timestamp <= end
    )
    
    # If admin, filter by organization
    if hasattr(current_user, 'api_key'):
        query = query.filter(models.Screenshot.organizationId == current_user.organizationId)
    # If employee, only show their screenshots
    else:
        query = query.filter(models.Screenshot.employeeId == current_user.id)
    
    screenshots = query.limit(limit).all()
    return screenshots


@router.delete("/{screenshot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_screenshot(
    screenshot_id: str,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_employee_user),
) -> Any:
    """
    Delete screenshot.
    """
    screenshot = db.query(models.Screenshot).filter(models.Screenshot.id == screenshot_id).first()
    if not screenshot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Screenshot not found",
        )
    
    # Check if user has access to the screenshot
    if hasattr(current_user, 'api_key'):  # Admin
        if screenshot.organizationId != current_user.organizationId:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to delete this screenshot",
            )
    else:  # Employee
        if screenshot.employeeId != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot delete screenshot for another employee",
            )
    
    # Update shift to increment deletedScreenshots counter
    shift = db.query(models.Shift).filter(models.Shift.id == screenshot.shiftId).first()
    if shift:
        shift.deletedScreenshots = (shift.deletedScreenshots or 0) + 1
    
    db.delete(screenshot)
    db.commit()
    return None


@router.get("/paginate", response_model=schemas.ScreenshotResponse)
def paginate_screenshots(
    start: int = Query(..., description="Start time in milliseconds"),
    end: int = Query(..., description="End time in milliseconds"),
    timezone: Optional[str] = None,
    task_id: Optional[str] = None,
    shift_id: Optional[str] = None,
    project_id: Optional[str] = None,
    sort_by: Optional[str] = None,
    limit: int = Query(10000, description="Maximum number of screenshots to return"),
    next: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_employee_user),
) -> Any:
    """
    Paginate screenshots.
    """
    query = db.query(models.Screenshot).filter(
        models.Screenshot.timestamp >= start,
        models.Screenshot.timestamp <= end
    )
    
    # Apply filters
    if task_id:
        # Handle comma-separated task IDs
        task_ids = task_id.split(",")
        query = query.filter(models.Screenshot.taskId.in_(task_ids))
    
    if shift_id:
        # Handle comma-separated shift IDs
        shift_ids = shift_id.split(",")
        query = query.filter(models.Screenshot.shiftId.in_(shift_ids))
    
    if project_id:
        # Handle comma-separated project IDs
        project_ids = project_id.split(",")
        query = query.filter(models.Screenshot.projectId.in_(project_ids))
    
    # If admin, filter by organization
    if hasattr(current_user, 'api_key'):
        query = query.filter(models.Screenshot.organizationId == current_user.organizationId)
    # If employee, only show their screenshots
    else:
        query = query.filter(models.Screenshot.employeeId == current_user.id)
    
    # Apply sorting
    if sort_by:
        if sort_by == "timestamp":
            query = query.order_by(models.Screenshot.timestamp)
        elif sort_by == "timestamp_desc":
            query = query.order_by(models.Screenshot.timestamp.desc())
    else:
        # Default sorting by timestamp
        query = query.order_by(models.Screenshot.timestamp)
    
    # Apply pagination
    if next:
        # Decode the next token to get the last timestamp
        try:
            last_timestamp = int(next)
            query = query.filter(models.Screenshot.timestamp > last_timestamp)
        except ValueError:
            pass
    
    # Get screenshots
    screenshots = query.limit(limit + 1).all()
    
    # Check if there are more results
    has_more = len(screenshots) > limit
    if has_more:
        screenshots = screenshots[:limit]
        next_token = str(screenshots[-1].timestamp)
    else:
        next_token = None
    
    return {
        "data": screenshots,
        "next": next_token
    }