from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.models.base import BaseModel


class Board(BaseModel):
    """
    Model de Board Kanban
    Cada board pertence a um projeto e tem várias colunas
    """

    __tablename__ = "boards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)

    # Relacionamentos
    project = relationship("Project", back_populates="boards")
    columns = relationship("Column", back_populates="board", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Board {self.name}>"
