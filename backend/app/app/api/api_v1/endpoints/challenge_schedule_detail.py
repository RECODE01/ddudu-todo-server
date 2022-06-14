from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.schemas.schedule import ChallengeScheduleCreate


router = APIRouter()


@router.get("/", response_model=List[schemas.ChallengeScheduleDetail])
def get_challenge_requests(
    db: Session = Depends(deps.get_db),
    page: int = 1,
    per_page: int = 10,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    challenges = crud.challenge.get_multi_by_user(
        db=db, user_id=current_user.id, page=page, per_page=per_page
    )
    return challenges


@router.post("/challenge_id", response_model=schemas.Msg)
def create_challenge_schedule(
    *,
    db: Session = Depends(deps.get_db),
    challenge_schedule_in: ChallengeScheduleCreate,
    challenge_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new Challenge Schedule.
    """
    #권한 확인
    users = crud.challenge_users.get_multi_by_challenge(
        db=db, challenge_id=challenge_id)
    if len(users) < 1:
        raise HTTPException(status_code=404, detail="No users in challenge")
    result = crud.challenge_schedule_detail.create_with_user(
        db=db, obj_in=challenge_schedule_in, challenge_id=challenge_id)
    for user in users:
        crud.schedule.create_with_challenge(
            db=db, obj_in=challenge_schedule_in, user_id=user.id, challenge_info_id=result.id)
    return {"msg": "챌린지 일정 등록 성공"}


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
        raise HTTPException(
            status_code=404, detail="Challenge request is already accepted")
    if not challenge_request:
        raise HTTPException(status_code=404, detail="Challenge request not found")
    crud.challenge_request.accept_challenge_request(
        db=db, db_obj=challenge_request)
    crud.challenge_users.create_with_user(
        db=db, obj_in={"challenge_id": challenge_request.challenge_id}, user_id=current_user.id)
    crud.challenge_schedule_detail.get_multi()
    crud.schedule.create_with_challenge(db=db, user_id=challenge_request.user_id, )
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

@router.get("/{challenge_detail_id}/users", response_model=List[schemas.ChallengeScheduleComplete]) #response_model의 기능, 객체를 입력 보내준다.
def read_challenge_schedule_users(
        *,
        db: Session = Depends(deps.get_db),
        page: int = 0,
        per_page: int = 0,
        challenge_detail_id: int,
        # current_user: models.User = Depends(deps.get_current_active_user),
    ) -> Any :
        """
        맘껏 쓰세요~
        """

        challenge_schedule_complete = crud.challenge_schedule_detail.get_multi_by_complete_user(db=db, challenge_detail_id=challenge_detail_id, page=page, per_page=per_page)

        return challenge_schedule_complete

