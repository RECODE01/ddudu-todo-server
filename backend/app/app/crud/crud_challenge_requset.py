from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.challenge_request import ChallengeRequest
from app.schemas.challenge_request import ChallengeRequestCreate, ChallengeRequestUpdate


class CRUDChallengeRequest(CRUDBase[ChallengeRequest, ChallengeRequestCreate, ChallengeRequestUpdate]):
    def create_with_user(
        self, db: Session, *, obj_in: ChallengeRequestCreate, user_id: int
    ) -> ChallengeRequest:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return {"msg": "챌린지 참가 신청 완료"}

    def accept_challenge_request(
        self,
        db: Session,
        *,
        db_obj: ChallengeRequest,
    ) -> ChallengeRequest:
        setattr(db_obj, "is_accept", True)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj.is_accept

    def get_challenge_request(
        self,
        db: Session,
        *,
        challenge_id: int,
        user_id: int
    ) -> ChallengeRequest:
        return (db.query(self.model)
                .filter(self.model.challenge_id ==
                        challenge_id).filter(self.model.user_id == user_id)
                .one_or_none())

    def get_multi_by_challenge(
        self, db: Session, *, page: int = 1, per_page: int = 100, challenge_id: int
    ) -> List[ChallengeRequest]:
        if (page == 0):
            page = 1
        if page == 0 or page == 1:
            skip = 0
        else:
            skip = (page - 1) * per_page - 1
        return (db.query(self.model)
                .filter(self.model.challenge_id == challenge_id)
                .filter(self.model.is_accept == False)
                .offset(skip)
                .limit(per_page)
                .all())

    def get_multi_by_user(
        self, db: Session, *, user_id: int, page: int = 1, per_page: int = 100
    ) -> List[ChallengeRequest]:
        if (page == 0):
            page = 1
        if page == 0 or page == 1:
            skip = 0
        else:
            skip = (page - 1) * per_page - 1
        return (db.query(self.model)
                .filter(self.model.user_id == user_id)
                .filter(self.model.is_accept == False)
                .offset(skip)
                .limit(per_page)
                .all())


challenge_request = CRUDChallengeRequest(ChallengeRequest)
