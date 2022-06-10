from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Boolean
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.ChallengeRequestAccept])
def get_challenge_requests(
    db: Session = Depends(deps.get_db),
    page: int = 0,
    per_page: int = 0,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    challenges = crud.challenge.get_multi_by_user(
        db=db, user_id=current_user.id, page=page, per_page=per_page
    )
    return challenges


@router.post("/{challenge_id}", response_model=schemas.Msg)
def create_challenge_request(
    *,
    db: Session = Depends(deps.get_db),
    challenge_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new Challenge Request.
    """
    challenge_request = crud.challenge_request.get(
        db=db, challenge_id=challenge_id, user_id=current_user.id)
    if challenge_request:
        raise HTTPException(
            status_code=404, detail="Challenge request is already existed")
    result = crud.challenge_request.create_with_user(
        db=db, obj_in={"challenge_id": challenge_id}, user_id=current_user.id)
    return result


@router.post("/accept/{id}", response_model=schemas.Msg)
def accept_challenge_request(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Accept Challenge Request.
    """
    challenge_request = crud.challenge_request.get(db=db, id=id)
    print(challenge_request.is_accept)
    if challenge_request.is_accept is True:
        raise HTTPException(status_code=404, detail="Challenge request is already accepted")
    if not challenge_request:
        raise HTTPException(status_code=404, detail="Challenge request not found")
    # 권한 부분 함수화해서 일괄 수정 예정??????
    # if not crud.user.is_superuser(current_user) and (challenge_request.user_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    result = crud.challenge_request.accept_challenge_request(
        db=db, db_obj=challenge_request)
    crud.challenge_users.create_with_user(
        db=db, obj_in={"challenge_id": challenge_request.challenge_id}, user_id=current_user.id)
    return {"msg": "챌린지 참가 신청을 수락하였습니다."}


@router.delete("/refuse{id}", response_model=schemas.Msg)
def refuse_challenge_request(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    refuse challenge request.
    """
    challenge = crud.challenge.get(db=db, id=id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    if not crud.user.is_superuser(current_user) and (challenge.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    challenge = crud.challenge.remove(db=db, id=id)
    return {"msg": "챌린지 참가 신청을 거절하였습니다."}
