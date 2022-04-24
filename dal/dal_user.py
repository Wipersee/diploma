from models.user import User, UnauthorizedLogins
from validators import user_schema as schemas
from structlog import get_logger
from dal.database import db
from sqlalchemy import func

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

def get_unauth_by_user_id(id: str):
    try:
        return db.session.query(UnauthorizedLogins).filter(UnauthorizedLogins.user_id == id).all()
    except Exception as e:
        logger.exception(f"Error in unauthorized  get by user id {id} dal reason : {e}")
        return None

def get_unauth_by_user_id_for_pie(id: str):
    try:
        return db.session.query(
            UnauthorizedLogins.type,
            func.count(UnauthorizedLogins.date).filter(UnauthorizedLogins.user_id == id)
        ).group_by(UnauthorizedLogins.type
        ).all()
    except Exception as e:
        logger.exception(f"Error in unauthorized  get by user id {id} dal reason : {e}")
        return None

def get_unauth_by_user_id_for_line(id: str):
    try:
        return db.session.query(
            func.strftime("%Y-%m-%d", UnauthorizedLogins.date),
            func.count(UnauthorizedLogins.date).filter(UnauthorizedLogins.user_id == id)
        ).group_by(func.strftime("%Y-%m-%d", UnauthorizedLogins.date)).all()
    except Exception as e:
        logger.exception(f"Error in unauthorized  get by user id {id} dal reason : {e}")
        return None

def update(user: schemas.PutUser, user_id: str):
    try:
        db.session.query(User).filter(User.id == user_id).update(
            {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            }
        )
        db.session.commit()
        return True
    except Exception as e:
        logger.exception(f"Error while updating user {user_id} Reason: {e}")
        return False

def update_password(password: str, user_id: str):
    try:
        db.session.query(User).filter(User.id == user_id).update(
            {
                "password": password
            }
        )
        db.session.commit()
        return True
    except Exception as e:
        logger.exception(f"Error while updating user {user_id} password Reason: {e}")
        return False


def add(user: schemas.CreateUser):
    try:
        db.session.add(user)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logger.exception(f"Error in user add dal reason : {e}")
        return False


def add_unauthorized_logins(unauthorized_login):
    try:
        db.session.add(unauthorized_login)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logger.exception(f"Error in user add unauthorized_login dal reason : {e}")
        return False