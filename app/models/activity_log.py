from sqlalchemy import Column, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from app.models.base import BaseModel


class ActivityAction(enum.Enum):
    """Enum para tipos de ações no sistema"""

    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    TASK_DELETED = "task_deleted"
    TASK_MOVED = "task_moved"
    TASK_ASSIGNED = "task_assigned"
    COMMENT_ADDED = "comment_added"
    TAG_ADDED = "tag_added"
    TAG_REMOVED = "tag_removed"


class ActivityLog(BaseModel):
    """
    Model de Log de Atividades
    Registra todas as ações importantes no sistema
    """

    __tablename__ = "activity_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    action = Column(Enum(ActivityAction), nullable=False)
    description = Column(Text, nullable=True)
    meta_data = Column(Text, nullable=True)

    # Foreign Keys
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Relacionamentos
    task = relationship("Task", back_populates="activity_logs")
    user = relationship("User", back_populates="activity_logs")

    def __repr__(self):
        return f"<ActivityLog {self.action} by User {self.user_id}>"
