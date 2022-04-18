from models.user import User, Token
from validators import user_schema as schemas
from structlog import get_logger
from dal.database import db

logger = get_logger()


def add(token: Token):
    try:
        db.session.add(token)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logger.exception(f"Error in token add dal reason : {e}")
        return False

def get(user_id: str):
    try:
        return db.session.query(Token).filter(Token.user_id == user_id).first()
    except Exception as e:
        logger.exception(f"Error in token get dal reason : {e}")
        return None

def get_by_token(token: str):
    try:
        return db.session.query(Token).filter(Token.token == token).first()
    except Exception as e:
        logger.exception(f"Error in token get by token dal reason : {e}")
        return None

def delete(token: Token):
    try:
        db.session.delete(token)
        db.session.commit()
        return True
    except Exception as e:
        logger.exception(f"Error in token delete dal reason : {e}")
        return None