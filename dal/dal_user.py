from dal.database import database
from models.user import users
from validators import user_schema as schemas


async def get_user_by_email(email: str):
    return await database.fetch_one(users.select().where(users.c.email == email))


async def create_user(user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = users.insert().values(
        email=user.email, hashed_password=fake_hashed_password
    )
    user_id = await database.execute(db_user)
    return schemas.User(**user.dict(), id=user_id)
