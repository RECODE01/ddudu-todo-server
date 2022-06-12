from typing import List
from xmlrpc.client import Boolean

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.crud.crud_challenge_user_detail import challenge_users
from app.models.cahllenge import Challenge
from app.schemas.challenge import ChallengeCreate, ChallengeUpdate
from app.models.challenge_user_detail import ChallengeUserDetail
# from app.schemas.item import ItemCreate, ItemUpdate


class CRUDChallenge(CRUDBase[Challenge, ChallengeCreate, ChallengeUpdate]):
    def create_with_user(
        self, db: Session, *, obj_in: ChallengeCreate, user_id: int
    ) -> Challenge:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        challenge_users.create_with_user(
            db, obj_in={"challenge_id": db_obj.id, "is_master": True}, user_id=user_id)

        return db_obj

    def get_multi_by_user(
        self, db: Session, *, user_id: int, page: int = 0, per_page: int = 100
    ) -> List[Challenge]:
        return list(map(lambda ch: ch.challenge, db.query(ChallengeUserDetail)
        .filter(ChallengeUserDetail.user_id ==user_id)
        .offset(page)
        .limit(per_page)
        .all()))


challenge = CRUDChallenge(Challenge)
