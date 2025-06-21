from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.utils.id_generator import generate_id


# Association table for team-project relationship
team_project = Table(
    "team_project",
    Base.metadata,
    Column("team_id", String, ForeignKey("teams.id")),
    Column("project_id", String, ForeignKey("projects.id")),
)


class Team(Base):
    __tablename__ = "teams"

    id = Column(String, primary_key=True, index=True, default=lambda: generate_id("wt"))
    name = Column(String)
    organizationId = Column(String, index=True)
    createdAt = Column(Integer)  # Time in milliseconds
    
    # Relationships
    employees = relationship("Employee", back_populates="team")
    projects = relationship("Project", secondary=team_project, back_populates="teams")