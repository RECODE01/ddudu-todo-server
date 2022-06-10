from typing import List
from xmlrpc.client import Boolean

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

challenge_schedule_detail = CRUDChallengeSchedules(ChallengeScheduleDetail)
