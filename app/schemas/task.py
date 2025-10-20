from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID
from app.models.task import TaskPriority


# Schema base de tarefa
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None


# Schema para criar tarefa
class TaskCreate(TaskBase):
    column_id: UUID
    assignee_id: Optional[UUID] = None


# Schema para atualizar tarefa
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    assignee_id: Optional[UUID] = None


# Schema para mover tarefa entre colunas
class TaskMove(BaseModel):
    column_id: UUID
    position: int = Field(..., ge=0)


# Schema de resposta da tarefa
class TaskResponse(TaskBase):
    id: UUID
    position: int
    column_id: UUID
    assignee_id: Optional[UUID] = None
    created_by: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
