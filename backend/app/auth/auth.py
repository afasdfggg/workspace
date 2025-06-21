from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import verify_password, verify_api_key
from app.db.database import get_db
from app.models.employee import Employee
from app.models.admin import Admin

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


def authenticate_user(db: Session, email: str, password: str, is_admin: bool = False):
    if is_admin:
        user = db.query(Admin).filter(Admin.email == email).first()
    else:
        user = db.query(Employee).filter(Employee.email == email).first()
    
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_type = payload.get("type", "access")
        if token_type != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Check if user is admin
    admin = db.query(Admin).filter(Admin.id == user_id).first()
    if admin:
        return admin
    
    # Check if user is employee
    employee = db.query(Employee).filter(Employee.id == user_id).first()
    if employee is None:
        raise credentials_exception
    
    return employee


def get_current_admin(
    current_user = Depends(get_current_user),
):
    if not isinstance(current_user, Admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user


def get_current_employee(
    current_user = Depends(get_current_user),
):
    if not isinstance(current_user, Employee):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid employee credentials",
        )
    return current_user


def get_api_key_user(
    db: Session = Depends(get_db), api_key: str = Depends(api_key_header)
):
    if not api_key or not api_key.startswith("Bearer "):
        return None
    
    api_key = api_key.replace("Bearer ", "")
    user_id = verify_api_key(api_key)
    
    if not user_id:
        return None
    
    # Check if user is admin
    admin = db.query(Admin).filter(Admin.id == user_id).first()
    if admin:
        return admin
    
    return None