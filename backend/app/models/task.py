from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.utils.id_generator import generate_id


# Association table for employee-task relationship
employee_task = Table(
    "employee_task",
    Base.metadata,
    Column("employee_id", String, ForeignKey("employees.id")),
    Column("task_id", String, ForeignKey("tasks.id")),
)


# Association table for team-task relationship
team_task = Table(
    "team_task",
    Base.metadata,
    Column("team_id", String, ForeignKey("teams.id")),
    Column("task_id", String, ForeignKey("tasks.id")),
)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True, default=lambda: generate_id("wt"))
    status = Column(String, default="To Do")
    priority = Column(String, default="low")
    billable = Column(Boolean, default=True)
    name = Column(String)
    projectId = Column(String, ForeignKey("projects.id"))
    description = Column(String, nullable=True)
    creatorId = Column(String, ForeignKey("employees.id"))
    organizationId = Column(String, index=True)
    createdAt = Column(Integer)  # Time in milliseconds
    deadline = Column(Integer, nullable=True)  # Time in milliseconds
    labels = Column(JSON, default=lambda: [])
    
    # Relationships
    project = relationship("Project", back_populates="tasks")
    employees = relationship("Employee", secondary=employee_task, back_populates="tasks")
    teams = relationship("Team", secondary=team_task)
    shifts = relationship("Shift", back_populates="task")