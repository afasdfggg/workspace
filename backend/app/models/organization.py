from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.utils.id_generator import generate_id


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(String, primary_key=True, index=True, default=lambda: generate_id("wo"))
    name = Column(String)
    createdAt = Column(Integer)  # Time in milliseconds