from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel

from app.schemas.base import *


class PayrollInfo(BaseModel):
    billRate: Optional[float] = None
    overtimeBillRate: Optional[float] = None


class ScreenshotSettings(BaseModel):
    screenshotEnabled: bool = True


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    billable: bool = True
    organizationId: str


class ProjectCreate(ProjectBase):
    employees: Optional[List[str]] = []
    teams: Optional[List[str]] = []
    creatorId: str
    statuses: Optional[List[str]] = ["To do", "On hold", "In progress", "Done"]
    priorities: Optional[List[str]] = ["low", "medium", "high"]
    payroll: Optional[PayrollInfo] = None
    screenshotSettings: Optional[ScreenshotSettings] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    billable: Optional[bool] = None
    employees: Optional[List[str]] = None
    teams: Optional[List[str]] = None
    statuses: Optional[List[str]] = None
    priorities: Optional[List[str]] = None
    payroll: Optional[PayrollInfo] = None
    screenshotSettings: Optional[ScreenshotSettings] = None
    archived: Optional[bool] = None


class ProjectInDBBase(ProjectBase):
    id: str
    archived: bool = False
    statuses: List[str]
    priorities: List[str]
    payroll: Optional[PayrollInfo] = None
    creatorId: str
    employees: List[str] = []
    teams: List[str] = []
    createdAt: int
    screenshotSettings: ScreenshotSettings

    class Config:
        orm_mode = True


class Project(ProjectInDBBase):
    pass