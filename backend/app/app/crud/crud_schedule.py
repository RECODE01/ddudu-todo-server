from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate
# from app.schemas.item import ItemCreate, ItemUpdate


class CRUDSchedule(CRUDBase[Schedule, ScheduleCreate, ScheduleUpdate]):
    def create_with_user(
        self, db: Session, *, obj_in: ScheduleCreate, user_id: int
    ) -> Schedule:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_user(
        self, db: Session, *, user_id: int, page: int = 0, per_page: int = 100
    ) -> List[Schedule]:
        return (
            db.query(self.model)
            .filter(Schedule.user_id == user_id)
            .offset(page)
            .limit(per_page)
            .all()
        )


schedule = CRUDSchedule(Schedule)
