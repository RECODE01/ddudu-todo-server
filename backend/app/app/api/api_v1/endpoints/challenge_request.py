from datetime import datetime
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/me", response_model=List[schemas.ChallengeRequest])
def get_challenge_requests(
    *,
    db: Session = Depends(deps.get_db),
    page: int = 1,
    per_page: int = 10,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    requests = crud.challenge_request.get_multi_by_user(
        db=db, user_id=current_user.id, page=page, per_page=per_page
    )
    return requests


@router.get("/{challenge_id}", response_model=List[schemas.ChallengeRequest])
def get_challenge_requests(
    *,
    db: Session = Depends(deps.get_db),
    page: int = 1,
    challenge_id: int,
    per_page: int = 10,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    if not crud.challenge_users.get_is_challenge_master(db=db, challenge_id=challenge_id, user_id=current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    requests = crud.challenge_request.get_multi_by_challenge(
        db=db, page=page, per_page=per_page, challenge_id=challenge_id
    )
    return requests


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
    challenge_request = crud.challenge_request.get_challenge_request(
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
    if challenge_request.is_accept is True:
        raise HTTPException(
            status_code=404, detail="Challenge request is already accepted")
    if not challenge_request:
        raise HTTPException(status_code=404, detail="Challenge request not found")
    if not crud.challenge_users.get_is_challenge_master(db=db, challenge_id=challenge_request.challenge_id, user_id=current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    crud.challenge_request.accept_challenge_request(
        db=db, db_obj=challenge_request)
    crud.challenge_users.create_with_user(
        db=db, obj_in={"challenge_id": challenge_request.challenge_id}, user_id=current_user.id)
    schedules = crud.challenge_schedule_detail.get_multi_by_date(
        db=db, date=datetime.now(), challenge_id=challenge_request.challenge_id)
    for schedule in schedules:
        crud.schedule.create_with_challenge(db=db, obj_in={
            "title": schedule.title,
            "contents": schedule.contents,
            "image": schedule.image,
            "start_date": schedule.start_date,
            "end_date": schedule.end_date,
        }, user_id=challenge_request.user_id, challenge_info_id=schedule.id)
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
    if not crud.challenge_users.get_is_challenge_master(db=db, challenge_id=challenge.id, user_id=current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    challenge = crud.challenge.remove(db=db, id=id)
    return {"msg": "챌린지 참가 신청을 거절하였습니다."}
