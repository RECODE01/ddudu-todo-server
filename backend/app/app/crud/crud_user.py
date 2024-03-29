from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from sqlalchemy.sql import text


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get(self, db: Session, id: int) -> User :
        return(db.execute(text(
            """
                WITH schedule_cnt AS (
                select
                    (select 
                		count(*) 
                	from 
                 		schedule 
                 	where 
                		user_id = :id) as scheduleCnt, 
                	(select 
                		count(*) 
                	from 
                		schedule 
                	where 
                		user_id = :id and  
                		completed is TRUE) as completeCnt
                )
                select 
                	"user".*,
                	case when schedule_cnt.scheduleCnt < 1 then 0 :: decimal
                	else schedule_cnt.completeCnt / schedule_cnt.scheduleCnt :: decimal  
                	end as complete_rate
                from 
                	"user"
                	cross join
                		schedule_cnt
                where 
                	"user".id = :id;
            """), {'id':id}).fetchone())
        
        

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            name=obj_in.name,
            nick_name=obj_in.nick_name,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
