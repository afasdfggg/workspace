from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, EmailStr, Field

from app.schemas.base import *


class SystemPermission(BaseModel):
    computer: str
    permissions: Dict[str, str]
    createdAt: int
    updatedAt: int


class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    teamId: Optional[str] = None
    sharedSettingsId: Optional[str] = None
    accountId: Optional[str] = None
    identifier: Optional[str] = None
    type: str = "personal"  # Values are "personal" or "office"
    organizationId: str
    title: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    projects: Optional[List[str]] = []


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    teamId: Optional[str] = None
    sharedSettingsId: Optional[str] = None
    title: Optional[str] = None
    projects: Optional[List[str]] = None


class EmployeeInDBBase(EmployeeBase):
    id: str
    deactivated: Optional[int] = None
    invited: Optional[int] = None
    systemPermissions: Optional[List[SystemPermission]] = None
    createdAt: int
    projects: List[str] = []

    class Config:
        orm_mode = True


class Employee(EmployeeInDBBase):
    pass


class EmployeeSetPassword(BaseModel):
    password: str


class EmployeeLogin(BaseModel):
    email: EmailStr
    password: str