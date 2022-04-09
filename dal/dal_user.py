from dal.database import database
from models.user import User
from validators import user_schema as schemas
from utils.hashing import Hasher


async def create_user(user: schemas.CreateUser):
    hashed_password = Hasher.get_password_hash(user.password)
    db_user = User.__table__.insert().values(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        active=user.active,
        password=hashed_password,
    )
    user_id = await database.execute(db_user)
    return schemas.CreateUser(**user.dict(), id=user_id)
