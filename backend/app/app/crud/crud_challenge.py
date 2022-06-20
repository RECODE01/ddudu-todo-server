from doctest import master
from typing import List
from xmlrpc.client import Boolean

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.crud.crud_challenge_user_detail import challenge_users
from app.models.cahllenge import Challenge
from app.schemas.challenge import ChallengeCreate, ChallengeUpdate, Challenge as ChallengeReturn
from app.models.challenge_user_detail import ChallengeUserDetail
from app.schemas import challenge
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

    def get_multi(self, db: Session, *, page: int = 1, per_page: int = 100) -> List[Challenge]:
        if (page == 0):
            page = 1
        if page == 0 or page == 1:
            skip = 0
        else:
            skip = (page - 1) * per_page - 1
        challenge_list = super().get_multi(db, skip=skip, limit=per_page)
        result = []
        for i in range(len(challenge_list)):
            challenge_id = challenge_list[i].id
            master = db.query(ChallengeUserDetail).filter(ChallengeUserDetail.challenge_id == challenge_id).filter(ChallengeUserDetail.is_master == True).one()
            user_cnt = db.query(ChallengeUserDetail).filter(ChallengeUserDetail.challenge_id == challenge_id).count()
            master = master.user

            challenge = ChallengeReturn
            challenge.id = challenge_list[i].id
            challenge.contents =  challenge_list[i].contents
            challenge.end_date =  challenge_list[i].end_date
            challenge.image =  challenge_list[i].image
            challenge.master = master
            challenge.name = challenge_list[i].name
            challenge.start_date = challenge_list[i].start_date
            challenge.tags =  challenge_list[i].tags
            challenge.user_cnt = user_cnt
            result.append(challenge)

        return result

    def get_multi_by_user(
        self, db: Session, *, user_id: int, page: int = 1, per_page: int = 100
    ) -> List[Challenge]:

        challenge_list = list(map(lambda ch: ch.challenge, db.query(ChallengeUserDetail)
                            .filter(ChallengeUserDetail.user_id == user_id)
                            .offset(page)
                            .limit(per_page)
                            .all()))
        
        result = []
        for i in range(len(challenge_list)):
            challenge_id = challenge_list[i].id
            master = db.query(ChallengeUserDetail).filter(ChallengeUserDetail.challenge_id == challenge_id).filter(ChallengeUserDetail.is_master == True).one()
            user_cnt = db.query(ChallengeUserDetail).filter(ChallengeUserDetail.challenge_id == challenge_id).count()
            master = master.user

            challenge = ChallengeReturn
            challenge.id = challenge_list[i].id
            challenge.contents =  challenge_list[i].contents
            challenge.end_date =  challenge_list[i].end_date
            challenge.image =  challenge_list[i].image
            challenge.master = master
            challenge.name = challenge_list[i].name
            challenge.start_date = challenge_list[i].start_date
            challenge.tags =  challenge_list[i].tags
            challenge.user_cnt = user_cnt
            result.append(challenge)

        return result

challenge = CRUDChallenge(Challenge)
