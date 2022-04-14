from models.application import Application
from models.user import User
from validators import user_schema as schemas
from utils.hashing import Hasher
from sqlalchemy.orm.session import Session
from structlog import get_logger

logger = get_logger()


async def get(session: Session):
    try:
        return session.query(User).all()
    except Exception as e:
        logger.exception(f"Error in user get all dal reason : {e}")
        return None


async def get_by_name(session: Session, username: str):
    try:
        return session.query(User).filter(User.username == username).first()
    except Exception as e:
        logger.exception(f"Error in user get by username {username} dal reason : {e}")
        return None


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
        logger.exception(f"Error in user add dal reason : {e}")
        return False

async def delete(session: Session, app_id: int):
    try:
        session.query(Application).delete().where(Application.id==app_id)
        return True
    except Exception as e:
        logger.exception(f"Delete app exception reason {e}")
        return False