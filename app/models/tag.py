from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.models.base import BaseModel
from app.core.database import Base


# Tabela de associação Many-to-Many entre Task e Tag
task_tags = Table(
    "task_tags",
    Base.metadata,
    Column("task_id", UUID(as_uuid=True), ForeignKey("tasks.id"), primary_key=True),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id"), primary_key=True),
)


class Tag(BaseModel):
    """
    Model de Tag/Label para categorizar tarefas
    """

    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    color = Column(String(7), nullable=False, default="#3B82F6")
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)

    # Relacionamentos
    project = relationship("Project", back_populates="tags")
    tasks = relationship("TaskTag", back_populates="tag")

    def __repr__(self):
        return f"<Tag {self.name}>"


class TaskTag(Base):
    """
    Model de associação entre Task e Tag
    """

    __tablename__ = "task_tags_association"

    task_id = Column(
        UUID(as_uuid=True), ForeignKey("tasks.id"), primary_key=True, nullable=False
    )
    tag_id = Column(
        UUID(as_uuid=True), ForeignKey("tags.id"), primary_key=True, nullable=False
    )

    # Relacionamentos
    task = relationship("Task", back_populates="tags")
    tag = relationship("Tag", back_populates="tasks")

    def __repr__(self):
        return f"<TaskTag task={self.task_id} tag={self.tag_id}>"
