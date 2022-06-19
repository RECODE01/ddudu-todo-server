from typing import List
from xmlrpc.client import Boolean

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.chatting_history import ChattingHistory
from app.schemas.chatting_history import ChattingHistoryCreate, ChattingHistoryUpdate

class CRUChattingDHistory(CRUDBase[ChattingHistory, ChattingHistoryCreate, ChattingHistoryUpdate]):
    def create_with_user_in_challenge(
        self, db: Session, *, obj_in: ChattingHistoryCreate, challenge_id: int, user_id: int
    ) -> ChattingHistory:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, challenge_id=challenge_id, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj
    
    def get_multi_by_challenge(
        self, db: Session, *, challenge_id: int, page: int = 1, per_page: int = 100
    ) -> List[ChattingHistory]:
        if (page == 0):
            page = 1
        if page == 0 or page == 1:
            skip = 0
        else:
            skip = (page - 1) * per_page - 1
        return  (db.query(self.model)
                .filter(ChattingHistory.challenge_id == challenge_id)
                .offset(skip)
                .limit(per_page)
                .all()
                )

chatting_history = CRUChattingDHistory(ChattingHistory)