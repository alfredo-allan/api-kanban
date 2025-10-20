from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.task import Task
from app.models.column import Column
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskMove
from app.middleware.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Criar nova tarefa
    """
    # Verificar se a coluna existe
    column = db.query(Column).filter(Column.id == task_data.column_id).first()
    if not column:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Column not found")

    # Calcular posição (última posição + 1)
    last_task = (
        db.query(Task)
        .filter(Task.column_id == task_data.column_id)
        .order_by(Task.position.desc())
        .first()
    )
    position = (last_task.position + 1) if last_task else 0

    # Criar tarefa
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        due_date=task_data.due_date,
        column_id=task_data.column_id,
        assignee_id=task_data.assignee_id,
        created_by=current_user.id,
        position=position,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.get("/", response_model=List[TaskResponse])
def list_tasks(
    column_id: Optional[str] = Query(None, description="Filter by column ID"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    assignee_id: Optional[str] = Query(None, description="Filter by assignee"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Listar tarefas com filtros opcionais
    """
    query = db.query(Task)

    # Aplicar filtros
    if column_id:
        query = query.filter(Task.column_id == column_id)
    if priority:
        query = query.filter(Task.priority == priority)
    if assignee_id:
        query = query.filter(Task.assignee_id == assignee_id)

    # Ordenar por posição
    query = query.order_by(Task.position)

    # Paginação
    tasks = query.offset(skip).limit(limit).all()

    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Buscar tarefa por ID
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: str,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Atualizar tarefa
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    # Atualizar campos
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


@router.patch("/{task_id}/move", response_model=TaskResponse)
def move_task(
    task_id: str,
    move_data: TaskMove,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Mover tarefa para outra coluna e/ou posição
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    # Verificar se a coluna existe
    column = db.query(Column).filter(Column.id == move_data.column_id).first()
    if not column:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Column not found")

    old_column_id = task.column_id
    old_position = task.position

    # Atualizar coluna e posição
    task.column_id = move_data.column_id
    task.position = move_data.position

    # Reorganizar posições na coluna antiga
    if old_column_id != move_data.column_id:
        db.query(Task).filter(Task.column_id == old_column_id, Task.position > old_position).update(
            {Task.position: Task.position - 1}
        )

    # Reorganizar posições na nova coluna
    db.query(Task).filter(
        Task.column_id == move_data.column_id,
        Task.position >= move_data.position,
        Task.id != task_id,
    ).update({Task.position: Task.position + 1})

    db.commit()
    db.refresh(task)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Deletar tarefa
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    # Reorganizar posições das tarefas restantes
    db.query(Task).filter(Task.column_id == task.column_id, Task.position > task.position).update(
        {Task.position: Task.position - 1}
    )

    db.delete(task)
    db.commit()

    return None


@router.get("/{column_id}/tasks", response_model=List[TaskResponse])
def get_tasks_by_column(
    column_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Buscar tasks por coluna
    """
    column = db.query(Column).filter(Column.id == column_id).first()
    if not column:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Column not found")

    tasks = db.query(Task).filter(Task.column_id == column_id).order_by(Task.position).all()

    return tasks
