import sched
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Boolean
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Schedule])
def read_schedules(
    db: Session = Depends(deps.get_db),
    page: int = 1,
    per_page: int = 10,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve Schedules.
    """
    schedules = crud.schedule.get_multi_by_user(
        db=db, user_id=current_user.id, page=page, per_page=per_page
    )
    return schedules


@router.post("/", response_model=schemas.Schedule)
def create_schedules(
    *,
    db: Session = Depends(deps.get_db),
    schedule_in: schemas.ScheduleCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new Schedule.
    """
    schedule = crud.schedule.create_with_user(db=db, obj_in=schedule_in, user_id=current_user.id)
    return schedule


@router.put("/{id}", response_model=schemas.Schedule)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    schedule_in: schemas.ScheduleUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an Schedule.
    """
    schedule = crud.schedule.get(db=db, id=id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    # if schedule.challenge_info_id is not None and schedule.challenge_info.challenge != current_user.id:
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    if not crud.user.is_superuser(current_user) and (schedule.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item = crud.schedule.update(db=db, db_obj=schedule, obj_in=schedule_in)
    return item


@router.get("/{id}", response_model=schemas.Schedule)
def read_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get schedule by ID.
    """
    schedule = crud.schedule.get(db=db, id=id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    if not crud.user.is_superuser(current_user) and (schedule.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return schedule


@router.delete("/{id}", response_model=schemas.Schedule)
def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an schedule.
    """
    schedule = crud.schedule.get(db=db, id=id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    if not crud.user.is_superuser(current_user) and (schedule.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    schedule = crud.schedule.remove(db=db, id=id)
    return schedule

@router.post("/toggle-complete/{id}", response_model=schemas.Schedule)
def toggle_schedule(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    toggle schedule complete value.
    """
    schedule = crud.schedule.get(db=db, id=id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    if not crud.user.is_superuser(current_user) and (schedule.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return crud.schedule.toggle_schedule_complete(db=db, db_obj=schedule)