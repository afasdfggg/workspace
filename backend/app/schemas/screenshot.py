from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel

from app.schemas.base import *


class SystemPermissions(BaseModel):
    accessibility: Optional[str] = None  # Options: authorized, denied, undetermined
    screenAndSystemAudioRecording: Optional[str] = None  # Options: authorized, denied, undetermined


class ScreenshotBase(BaseModel):
    employeeId: str
    shiftId: str
    timestamp: int  # Time in milliseconds
    organizationId: str


class ScreenshotCreate(ScreenshotBase):
    site: Optional[str] = None
    productivity: Optional[float] = None
    appId: Optional[str] = None
    appOrgId: Optional[str] = None
    appTeamId: Optional[str] = None
    teamId: Optional[str] = None
    srcEmployeeId: Optional[str] = None
    srcTeamId: Optional[str] = None
    timestampTranslated: Optional[str] = None
    systemPermissions: Optional[SystemPermissions] = None
    projectId: Optional[str] = None
    taskId: Optional[str] = None
    app: Optional[str] = None
    appFileName: Optional[str] = None
    appFilePath: Optional[str] = None
    title: Optional[str] = None
    url: Optional[str] = None
    document: Optional[str] = None
    windowId: Optional[str] = None
    taskStatus: Optional[str] = None
    taskPriority: Optional[str] = None
    user: Optional[str] = None
    computer: Optional[str] = None
    domain: Optional[str] = None
    name: Optional[str] = None
    hwid: Optional[str] = None
    os: Optional[str] = None
    osVersion: Optional[str] = None
    active: bool = True
    processed: bool = False
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None


class ScreenshotInDBBase(ScreenshotBase):
    id: str
    site: Optional[str] = None
    productivity: Optional[float] = None
    appId: Optional[str] = None
    appOrgId: Optional[str] = None
    appTeamId: Optional[str] = None
    teamId: Optional[str] = None
    srcEmployeeId: Optional[str] = None
    srcTeamId: Optional[str] = None
    timestampTranslated: Optional[str] = None
    systemPermissions: Optional[SystemPermissions] = None
    next: Optional[str] = None  # Hash value for pagination
    projectId: Optional[str] = None
    taskId: Optional[str] = None
    app: Optional[str] = None
    appFileName: Optional[str] = None
    appFilePath: Optional[str] = None
    title: Optional[str] = None
    url: Optional[str] = None
    document: Optional[str] = None
    windowId: Optional[str] = None
    taskStatus: Optional[str] = None
    taskPriority: Optional[str] = None
    user: Optional[str] = None
    computer: Optional[str] = None
    domain: Optional[str] = None
    name: Optional[str] = None
    hwid: Optional[str] = None
    os: Optional[str] = None
    osVersion: Optional[str] = None
    active: bool = True
    processed: bool = False
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None

    class Config:
        orm_mode = True


class Screenshot(ScreenshotInDBBase):
    pass


class ScreenshotResponse(BaseModel):
    data: List[Screenshot]
    next: Optional[str] = None