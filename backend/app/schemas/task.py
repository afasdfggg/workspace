from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel

from app.schemas.base import *


class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    projectId: str
    status: str = "To Do"
    priority: str = "low"
    billable: bool = True
    organizationId: str


class TaskCreate(TaskBase):
    employees: Optional[List[str]] = []
    teams: Optional[List[str]] = []
    creatorId: str
    deadline: Optional[int] = None
    labels: Optional[List[str]] = []


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    employees: Optional[List[str]] = None
    deadline: Optional[int] = None
    status: Optional[str] = None
    labels: Optional[List[str]] = None
    priority: Optional[str] = None
    billable: Optional[bool] = None


class TaskInDBBase(TaskBase):
    id: str
    creatorId: str
    employees: List[str] = []
    teams: List[str] = []
    createdAt: int
    deadline: Optional[int] = None
    labels: List[str] = []

    class Config:
        orm_mode = True


class Task(TaskInDBBase):
    pass