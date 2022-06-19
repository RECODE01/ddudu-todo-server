from typing import Any, List
from app.models import chatting_history

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Boolean
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


# @router.get("/my", response_model=List[schemas.ChattingHistory])

@router.post("/{challenge_id}", response_model=schemas.ChattingHistory)
def create_chatting_history(
  *,
  db: Session = Depends(deps.get_db),
  chatting_history_in : schemas.ChattingHistoryCreate,
  challenge_id : int,
  current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
  """
  Create new Chatting History.
  """
  chatting_history = crud.chatting_history.create_with_user_in_challenge(db=db, obj_in=chatting_history_in, challenge_id=challenge_id, user_id=current_user.id)
  return chatting_history

@router.get("/{challenge_id}", response_model=List[schemas.ChattingHistory])
def read_chatting_history(
    challenge_id : int,
    db: Session = Depends(deps.get_db),
    page: int = 1,
    per_page: int = 10,
) -> Any:
  """
  Read Chatting History
  """
  chatting_history = crud.chatting_history.get_multi_by_challenge(
    db=db, challenge_id=challenge_id, page=page, per_page=per_page
  )
  return chatting_history

@router.delete("/{chatting_history_id}", response_model=schemas.Msg)
def remove_chatting_history(
    chatting_history_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a Chatting History
    """
    deleted_chatting = crud.chatting_history.remove(db=db, id=chatting_history_id)
    
    if deleted_chatting is None:
        raise HTTPException(status_code=400, detail="메시지 삭제에 실패했습니다.")
    return {"msg": "메세지가 삭제됐습니다."}

@router.patch("/{chatting_history_id}", response_model=schemas.ChattingHistory)
def update_chatting_history(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    chatting_history_id: int,
    chatting_history_in: schemas.ChattingHistoryUpdate,
) -> Any:
  """
  Delete a Chatting History
  """
  chatting_history = crud.chatting_history.get(db=db, id=chatting_history_id)
  if not chatting_history:
      raise HTTPException(status_code=404, detail="Chatting not found")
  if (chatting_history.user_id != current_user.id):
      raise HTTPException(status_code=400, detail="Not enough permissions")
  chatting = crud.chatting_history.update(db=db, db_obj=chatting_history, obj_in=chatting_history_in)
  return chatting