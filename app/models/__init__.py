"""
Models do banco de dados
Importar todos aqui para o Alembic detectar automaticamente
"""

from app.models.base import BaseModel, TimestampMixin
from app.models.user import User
from app.models.project import Project
from app.models.board import Board
from app.models.column import Column
from app.models.task import Task, TaskPriority
from app.models.tag import Tag, TaskTag
from app.models.comment import Comment
from app.models.activity_log import ActivityLog, ActivityAction

__all__ = [
    "BaseModel",
    "TimestampMixin",
    "User",
    "Project",
    "Board",
    "Column",
    "Task",
    "TaskPriority",
    "Tag",
    "TaskTag",
    "Comment",
    "ActivityLog",
    "ActivityAction",
]
