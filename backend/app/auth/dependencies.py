from typing import Optional, Union

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.auth import get_current_admin, get_current_employee, get_api_key_user
from app.db.database import get_db
from app.models.admin import Admin
from app.models.employee import Employee


def get_admin_user(
    current_admin: Admin = Depends(get_current_admin),
    api_key_user: Optional[Admin] = Depends(get_api_key_user),
) -> Admin:
    """
    Get the current admin user from either JWT token or API key.
    """
    if api_key_user:
        return api_key_user
    return current_admin


def get_employee_user(
    current_employee: Employee = Depends(get_current_employee),
) -> Employee:
    """
    Get the current employee user from JWT token.
    """
    return current_employee


def check_employee_access(
    employee_id: str,
    current_user: Union[Admin, Employee] = Depends(get_current_admin),
    db: Session = Depends(get_db),
) -> Employee:
    """
    Check if the current user has access to the employee data.
    Admin users have access to all employees.
    Employee users only have access to their own data.
    """
    if isinstance(current_user, Admin):
        employee = db.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found",
            )
        return employee
    
    if current_user.id != employee_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this employee data",
        )
    
    return current_user