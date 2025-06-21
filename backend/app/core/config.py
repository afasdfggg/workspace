import os
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, EmailStr, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database settings
    DATABASE_URL: str
    
    # Admin settings
    ADMIN_EMAIL: EmailStr
    ADMIN_PASSWORD: str
    
    # Server settings
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 12000
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()