from models.user import User
from validators import user_schema as schemas
from structlog import get_logger
from dal.database import db

logger = get_logger()


def get():
    try:
        return db.session.query(User).all()
    except Exception as e:
        logger.exception(f"Error in user get all dal reason : {e}")
        return None


def get_by_name(username: str):
    try:
        return db.session.query(User).filter(User.username == username).first()
    except Exception as e:
        logger.exception(f"Error in user get by username {username} dal reason : {e}")
        return None

def get_by_id(id: str):
    try:
        return db.session.query(User).filter(User.id == id).first()
    except Exception as e:
        logger.exception(f"Error in user get by id {id} dal reason : {e}")
        return None

def add(user: schemas.CreateUser):
    try:
        db.session.add(user)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logger.exception(f"Error in user add dal reason : {e}")
        return False

