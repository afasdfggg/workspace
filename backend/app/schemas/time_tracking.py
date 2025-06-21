from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel

from app.schemas.base import *


class ShiftBase(BaseModel):
    type: str = "manual"  # Values: manual, automated, scheduled, leave
    start: int  # Time in milliseconds when shift started
    timezoneOffset: int  # Timezone difference in milliseconds
    employeeId: str
    organizationId: str
    projectId: Optional[str] = None
    taskId: Optional[str] = None


class ShiftCreate(ShiftBase):
    token: Optional[str] = None
    name: Optional[str] = None
    user: Optional[str] = None
    domain: Optional[str] = None
    computer: Optional[str] = None
    hwid: Optional[str] = None
    os: Optional[str] = None
    osVersion: Optional[str] = None
    paid: bool = True
    payRate: Optional[float] = None
    overtimePayRate: Optional[float] = None
    overtimeStart: Optional[int] = None
    teamId: Optional[str] = None


class ShiftUpdate(BaseModel):
    end: Optional[int] = None  # Time in milliseconds when shift ended
    projectId: Optional[str] = None
    taskId: Optional[str] = None


class ShiftInDBBase(ShiftBase):
    id: str
    token: Optional[str] = None
    end: Optional[int] = None  # Time in milliseconds when shift ended
    name: Optional[str] = None
    user: Optional[str] = None
    domain: Optional[str] = None
    computer: Optional[str] = None
    hwid: Optional[str] = None
    os: Optional[str] = None
    osVersion: Optional[str] = None
    paid: bool = True
    payRate: Optional[float] = None
    overtimePayRate: Optional[float] = None
    overtimeStart: Optional[int] = None
    teamId: Optional[str] = None
    startTranslated: Optional[int] = None
    endTranslated: Optional[int] = None
    overtimeStartTranslated: Optional[int] = None
    negativeTime: Optional[int] = None
    deletedScreenshots: Optional[int] = None
    lastActivityEnd: Optional[int] = None
    lastActivityEndTranslated: Optional[int] = None

    class Config:
        orm_mode = True


class Shift(ShiftInDBBase):
    pass


class ProjectTime(BaseModel):
    projectId: str
    projectName: str
    taskId: Optional[str] = None
    taskName: Optional[str] = None
    employeeId: str
    employeeName: str
    time: int  # Time in milliseconds
    date: int  # Date in milliseconds