from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.utils.id_generator import generate_id


# Association table for employee-project relationship
employee_project = Table(
    "employee_project",
    Base.metadata,
    Column("employee_id", String, ForeignKey("employees.id")),
    Column("project_id", String, ForeignKey("projects.id")),
)


class Employee(Base):
    __tablename__ = "employees"

    id = Column(String, primary_key=True, index=True, default=lambda: generate_id("we"))
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=True)
    teamId = Column(String, ForeignKey("teams.id"), nullable=True)
    sharedSettingsId = Column(String, nullable=True)
    accountId = Column(String, nullable=True)
    identifier = Column(String, nullable=True)
    type = Column(String, default="personal")  # Values are "personal" or "office"
    organizationId = Column(String, index=True)
    deactivated = Column(Integer, nullable=True)  # Time in milliseconds since deactivation
    invited = Column(Integer, nullable=True)  # Time in milliseconds from invitation to acceptance
    systemPermissions = Column(JSON, nullable=True)
    createdAt = Column(Integer)  # Time in milliseconds when employee was created
    title = Column(String, nullable=True)  # Job title
    
    # Relationships
    projects = relationship("Project", secondary=employee_project, back_populates="employees")
    tasks = relationship("Task", secondary="employee_task", back_populates="employees")
    team = relationship("Team", back_populates="employees")
    shifts = relationship("Shift", back_populates="employee")