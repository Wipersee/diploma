from models.user import User
from validators import user_schema as schemas
from utils.hashing import Hasher
from sqlalchemy.orm.session import Session


async def get(session: Session):
    try:
        return session.query(User).all()
    except Exception:
        return []

async def add(session: Session, user: schemas.CreateUser):
    try:
        hashed_password = Hasher.get_password_hash(user.password)
        db_user = User(
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            active=user.active,
            password=hashed_password,
        )
        session.add(db_user)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(e)
        return False
