from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Boolean
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Challenge])
def read_challenges(
    db: Session = Depends(deps.get_db),
    page: int = 0,
    per_page: int = 0,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve Challenges.
    """
    challenges = crud.challenge.get_multi_by_user(
        db=db, user_id=current_user.id, page=page, per_page=per_page
    )
    return challenges


@router.post("/", response_model=schemas.Challenge)
def create_challenges(
    *,
    db: Session = Depends(deps.get_db),
    challenge_in: schemas.ChallengeCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new Challenge.
    """
    challenge = crud.challenge.create_with_user(db=db, obj_in=challenge_in, user_id=current_user.id)
    return challenge

@router.post("/{challenge_id}/schedule", response_model=schemas.ChallengeScheduleDetail)
def create_challenge_schedule(
    *,
    db: Session = Depends(deps.get_db),
    challenge_in: schemas.ChallengeScheduleDetailCreate,
    challenge_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new challenge scheduele.
    """
    challenge_schedule = crud.challenge_schedule_detail.create_with_user(db=db, obj_in=challenge_in, challenge_id=challenge_id)
    challenge_users = crud.challenge_users.get_multi_by_challenge(db=db, challenge_id=challenge_id)

    for user in challenge_users:
        crud.schedule.create_with_challenge(db=db, user_id=user.id, obj_in=challenge_in , challenge_info_id=challenge_schedule.id)

    return challenge_schedule


# @router.put("/{id}", response_model=schemas.Challenge)
# def update_item(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     challenge_in: schemas.ChallengeUpdate,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Update an Challenge.
#     """
#     challenge = crud.challenge.get(db=db, id=id)
#     if not challenge:
#         raise HTTPException(status_code=404, detail="Challenge not found")
#     # if challenge.challenge_info_id is not None and challenge.challenge_info.challenge != current_user.id:
#     #     raise HTTPException(status_code=400, detail="Not enough permissions")
#     if not crud.user.is_superuser(current_user) and (challenge.user_id != current_user.id):
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     item = crud.challenge.update(db=db, db_obj=challenge, obj_in=challenge_in)
#     return item


@router.get("/{id}", response_model=schemas.Challenge)
def read_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get challenge by ID.
    """
    challenge = crud.challenge.get(db=db, id=id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    if not crud.user.is_superuser(current_user) and (challenge.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return challenge


@router.delete("/{id}", response_model=schemas.Challenge)
def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an challenge.
    """
    challenge = crud.challenge.get(db=db, id=id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    if not crud.user.is_superuser(current_user) and (challenge.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    challenge = crud.challenge.remove(db=db, id=id)
    return challenge

@router.patch("/toggle-complete/{id}", response_model=schemas.Challenge)
def toggle_challenge(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    toggle challenge complete value.
    """
    challenge = crud.challenge.get(db=db, id=id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    if not crud.user.is_superuser(current_user) and (challenge.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return crud.challenge.toggle_challenge_complete(db=db, db_obj=challenge)
