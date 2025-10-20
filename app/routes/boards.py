from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.board import Board
from app.models.project import Project
from app.models.user import User
from app.middleware.auth import get_current_user
from pydantic import BaseModel, Field
from uuid import UUID

router = APIRouter()


# Schemas
class BoardCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    project_id: UUID


class BoardResponse(BaseModel):
    id: UUID
    name: str
    project_id: UUID

    class Config:
        from_attributes = True


@router.get("/project/{project_id}", response_model=List[BoardResponse])
def list_boards_by_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Listar todos os boards de um projeto
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    boards = db.query(Board).filter(Board.project_id == project_id).all()
    return boards


@router.post("/", response_model=BoardResponse, status_code=status.HTTP_201_CREATED)
def create_board(
    board_data: BoardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Criar novo board
    """
    project = db.query(Project).filter(Project.id == board_data.project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    new_board = Board(name=board_data.name, project_id=board_data.project_id)

    db.add(new_board)
    db.commit()
    db.refresh(new_board)


@router.get("/{board_id}", response_model=BoardResponse)
def get_board(
    board_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Buscar board por ID
    """
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")

    # Verificar se o usuário tem acesso ao projeto do board
    project = db.query(Project).filter(Project.id == board.project_id).first()
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")

    return board
