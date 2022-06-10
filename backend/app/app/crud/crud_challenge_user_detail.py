from typing import List
from xmlrpc.client import Boolean

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.challenge_user_detail import ChallengeUserDetail
from app.schemas.challenge_user_detail import ChallengeUserDetailCreate, ChallengeUserDetailUpdate
# from app.schemas.item import ItemCreate, ItemUpdate


class CRUDChallengeUsers(CRUDBase[ChallengeUserDetail, ChallengeUserDetailCreate, ChallengeUserDetailUpdate]):
    def create_with_user(
        self, db: Session, *, obj_in: ChallengeUserDetailCreate, user_id: int
    ) -> ChallengeUserDetail:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

challenge_users = CRUDChallengeUsers(ChallengeUserDetail)
