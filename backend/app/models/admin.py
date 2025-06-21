from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.utils.id_generator import generate_id


class Admin(Base):
    __tablename__ = "admins"

    id = Column(String, primary_key=True, index=True, default=lambda: generate_id("wa"))
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    organizationId = Column(String, index=True)
    api_key = Column(String, nullable=True)
    createdAt = Column(Integer)  # Time in milliseconds