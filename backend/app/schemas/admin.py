from typing import Optional
from pydantic import BaseModel, EmailStr

from app.schemas.base import *


class AdminBase(BaseModel):
    email: EmailStr
    name: str
    organizationId: str


class AdminCreate(AdminBase):
    password: str


class AdminUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None


class AdminInDBBase(AdminBase):
    id: str
    createdAt: int

    class Config:
        orm_mode = True


class Admin(AdminInDBBase):
    pass


class AdminWithApiKey(Admin):
    api_key: str