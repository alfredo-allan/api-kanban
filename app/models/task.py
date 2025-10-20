from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from app.models.base import BaseModel


class TaskPriority(enum.Enum):
    """Enum para prioridades de tarefas"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(BaseModel):
    """
    Model de Tarefa
    Cada tarefa pertence a uma coluna do board
    """

    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    position = Column(Integer, nullable=False)
    priority = Column(
        Enum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False
    )
    due_date = Column(DateTime, nullable=True)

    # Foreign Keys
    column_id = Column(UUID(as_uuid=True), ForeignKey("columns.id"), nullable=False)
    assignee_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Relacionamentos
    column = relationship("Column", back_populates="tasks")
    assignee = relationship(
        "User", back_populates="assigned_tasks", foreign_keys=[assignee_id]
    )
    created_by_user = relationship(
        "User", back_populates="created_tasks", foreign_keys=[created_by]
    )
    tags = relationship("TaskTag", back_populates="task", cascade="all, delete-orphan")
    comments = relationship(
        "Comment", back_populates="task", cascade="all, delete-orphan"
    )
    activity_logs = relationship(
        "ActivityLog", back_populates="task", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Task {self.title}>"
