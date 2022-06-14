from datetime import date
from typing import List
from xmlrpc.client import Boolean
from app.schemas.challenge_schedule_detail import ChallengeScheduleComplete
from app.models.schedule import Schedule

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.challenge_schedule_detail import ChallengeScheduleDetail
from app.schemas.challenge_schedule_detail import ChallengeScheduleDetailCreate, ChallengeScheduleDetailUpdate
# from app.schemas.item import ItemCreate, ItemUpdate


class CRUDChallengeSchedules(CRUDBase[ChallengeScheduleDetail, ChallengeScheduleDetailCreate, ChallengeScheduleDetailUpdate]):
    def create_with_user(
        self, db: Session, *, obj_in: ChallengeScheduleDetailCreate, challenge_id: int
    ) -> ChallengeScheduleDetail:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, challenge_id=challenge_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_multi_by_challenge(
        self, db: Session, *, challenge_id: int, page:int = 1, per_page:int = 10
    ) -> List[ChallengeScheduleDetail]:
        if (page == 0):
            page = 1
        if page == 0 or page == 1:
            skip = 0
        else:
            skip = (page - 1) * per_page - 1
        return (
            db.query(ChallengeScheduleDetail)
            .filter(ChallengeScheduleDetail.challenge_id == challenge_id)
            .offset(skip)
            .limit(per_page)
            .all()
        )

    def get_multi_by_date(
        self, db: Session, *, date: date, challenge_id: int
    ) -> List[ChallengeScheduleDetail]:
        schedules = db.query(self.model).filter(
            self.model.challenge_id == challenge_id).filter(self.model.start_date < date).all()
        return schedules

    def get_multi_by_complete_user(
        self, db: Session, *, challenge_detail_id: int, page: int = 1, per_page: int = 10
    ) -> List[Schedule]:
        if (page == 0):
            page = 1
        if page == 0 or page == 1:
            skip = 0
        else:
            skip = (page - 1) * per_page - 1
        return (
            db.query(Schedule)
            .filter(Schedule.challenge_info_id == challenge_detail_id)
            .offset(skip)
            .limit(per_page)
            .all()
        )

challenge_schedule_detail = CRUDChallengeSchedules(ChallengeScheduleDetail)
