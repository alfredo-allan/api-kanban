from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.models.base import BaseModel


class Column(BaseModel):
    """
    Model de Coluna do Board (Backlog, A Fazer, Em Progresso, Concluído)
    """

    __tablename__ = "columns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable=False)
    position = Column(Integer, nullable=False)
    wip_limit = Column(Integer, nullable=True)
    board_id = Column(UUID(as_uuid=True), ForeignKey("boards.id"), nullable=False)

    # Relacionamentos
    board = relationship("Board", back_populates="columns")
    tasks = relationship("Task", back_populates="column", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Column {self.title}>"
