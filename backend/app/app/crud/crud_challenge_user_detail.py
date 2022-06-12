from typing import List
from xmlrpc.client import Boolean

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.challenge_user_detail import ChallengeUserDetail
from app.schemas.challenge_user_detail import ChallengeUserDetailCreate, ChallengeUserDetailUpdate
from app.models.user import User
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

    def get_multi_by_challenge(
        self, db: Session, *, challenge_id: str
    ) -> List[User]:
        details = db.query(self.model).filter(
            self.model.challenge_id == challenge_id).all()
        users = list(map(lambda el: el.user, details))
        return users

    def get_is_challenge_master(
        self, db: Session, *, challenge_id: str, user_id: str
    ) -> bool:
        details = (db.query(self.model)
                    .filter(self.model.challenge_id == challenge_id)
                    .filter(self.model.is_master == True)
                    .filter(user_id == user_id)
                    .all())
        return len(details) > 0

    def get_is_challenge_user(
        self, db: Session, *, challenge_id: str, user_id: str
    ) -> bool:
        details = (db.query(self.model)
                    .filter(self.model.challenge_id == challenge_id)
                    .filter(self.model.user_id == user_id).all())
        return len(details) > 0


challenge_users = CRUDChallengeUsers(ChallengeUserDetail)
