from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.column import Column
from app.models.board import Board
from app.models.user import User
from app.middleware.auth import get_current_user
from pydantic import BaseModel, Field
from uuid import UUID

router = APIRouter()


# Schemas
class ColumnCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    position: int = Field(..., ge=0)
    wip_limit: int | None = None
    board_id: UUID


class ColumnResponse(BaseModel):
    id: UUID
    title: str
    position: int
    wip_limit: int | None
    board_id: UUID

    class Config:
        from_attributes = True


@router.get("/board/{board_id}", response_model=List[ColumnResponse])
def list_columns_by_board(
    board_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Listar todas as colunas de um board
    """
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )

    columns = (
        db.query(Column)
        .filter(Column.board_id == board_id)
        .order_by(Column.position)
        .all()
    )

    return columns


@router.post("/", response_model=ColumnResponse, status_code=status.HTTP_201_CREATED)
def create_column(
    column_data: ColumnCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Criar nova coluna
    """
    board = db.query(Board).filter(Board.id == column_data.board_id).first()
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )

    new_column = Column(
        title=column_data.title,
        position=column_data.position,
        wip_limit=column_data.wip_limit,
        board_id=column_data.board_id,
    )

    db.add(new_column)
    db.commit()
    db.refresh(new_column)

    return new_column
