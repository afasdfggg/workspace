from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.utils.id_generator import generate_id


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(String, primary_key=True, index=True, default=lambda: generate_id("ws"))
    token = Column(String, nullable=True)
    type = Column(String, default="manual")  # Values: manual, automated, scheduled, leave
    start = Column(Integer)  # Time in milliseconds when shift started
    end = Column(Integer, nullable=True)  # Time in milliseconds when shift ended
    timezoneOffset = Column(Integer)  # Timezone difference in milliseconds
    name = Column(String, nullable=True)
    user = Column(String, nullable=True)
    domain = Column(String, nullable=True)
    computer = Column(String, nullable=True)
    hwid = Column(String, nullable=True)
    os = Column(String, nullable=True)
    osVersion = Column(String, nullable=True)
    paid = Column(Boolean, default=True)
    payRate = Column(Float, nullable=True)
    overtimePayRate = Column(Float, nullable=True)
    overtimeStart = Column(Integer, nullable=True)
    employeeId = Column(String, ForeignKey("employees.id"))
    teamId = Column(String, ForeignKey("teams.id"), nullable=True)
    organizationId = Column(String, index=True)
    startTranslated = Column(Integer, nullable=True)
    endTranslated = Column(Integer, nullable=True)
    overtimeStartTranslated = Column(Integer, nullable=True)
    negativeTime = Column(Integer, nullable=True)
    deletedScreenshots = Column(Integer, nullable=True)
    lastActivityEnd = Column(Integer, nullable=True)
    lastActivityEndTranslated = Column(Integer, nullable=True)
    projectId = Column(String, ForeignKey("projects.id"), nullable=True)
    taskId = Column(String, ForeignKey("tasks.id"), nullable=True)
    
    # Relationships
    employee = relationship("Employee", back_populates="shifts")
    task = relationship("Task", back_populates="shifts")
    screenshots = relationship("Screenshot", back_populates="shift", cascade="all, delete-orphan")