from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.utils.id_generator import generate_id


class Screenshot(Base):
    __tablename__ = "screenshots"

    id = Column(String, primary_key=True, index=True)
    site = Column(String, nullable=True)
    productivity = Column(Float, nullable=True)
    employeeId = Column(String, ForeignKey("employees.id"))
    appId = Column(String, nullable=True)
    appOrgId = Column(String, nullable=True)
    appTeamId = Column(String, nullable=True)
    teamId = Column(String, ForeignKey("teams.id"), nullable=True)
    organizationId = Column(String, index=True)
    srcEmployeeId = Column(String, nullable=True)
    srcTeamId = Column(String, nullable=True)
    timestampTranslated = Column(String, nullable=True)
    systemPermissions = Column(JSON, nullable=True)
    next = Column(String, nullable=True)  # Hash value for pagination
    timestamp = Column(Integer)  # Time in milliseconds
    shiftId = Column(String, ForeignKey("shifts.id"))
    projectId = Column(String, ForeignKey("projects.id"), nullable=True)
    taskId = Column(String, ForeignKey("tasks.id"), nullable=True)
    app = Column(String, nullable=True)
    appFileName = Column(String, nullable=True)
    appFilePath = Column(String, nullable=True)
    title = Column(String, nullable=True)
    url = Column(String, nullable=True)
    document = Column(String, nullable=True)
    windowId = Column(String, nullable=True)
    taskStatus = Column(String, nullable=True)
    taskPriority = Column(String, nullable=True)
    user = Column(String, nullable=True)
    computer = Column(String, nullable=True)
    domain = Column(String, nullable=True)
    name = Column(String, nullable=True)
    hwid = Column(String, nullable=True)
    os = Column(String, nullable=True)
    osVersion = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    processed = Column(Boolean, default=False)
    createdAt = Column(String, nullable=True)
    updatedAt = Column(String, nullable=True)
    
    # Relationships
    shift = relationship("Shift", back_populates="screenshots")