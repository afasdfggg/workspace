from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Table, JSON, ARRAY
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.utils.id_generator import generate_id
from app.models.employee import employee_project
from app.models.team import team_project


class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, index=True, default=lambda: generate_id("wp"))
    archived = Column(Boolean, default=False)
    statuses = Column(JSON, default=lambda: ["To do", "On hold", "In progress", "Done"])
    priorities = Column(JSON, default=lambda: ["low", "medium", "high"])
    billable = Column(Boolean, default=True)
    payroll = Column(JSON, nullable=True)
    name = Column(String)
    description = Column(String, nullable=True)
    creatorId = Column(String, ForeignKey("employees.id"))
    organizationId = Column(String, index=True)
    createdAt = Column(Integer)  # Time in milliseconds
    screenshotSettings = Column(JSON, default=lambda: {"screenshotEnabled": True})
    
    # Relationships
    employees = relationship("Employee", secondary=employee_project, back_populates="projects")
    teams = relationship("Team", secondary=team_project, back_populates="projects")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")