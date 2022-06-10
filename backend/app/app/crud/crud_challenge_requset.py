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


challenge_request = CRUDChallengeRequest(ChallengeRequest)
