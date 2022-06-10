from .crud_item import item
from .crud_user import user
from .crud_schedule import schedule
from .crud_challenge import challenge
from .crud_challenge_user_detail import challenge_users
from .crud_challenge_requset import  challenge_request
# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
