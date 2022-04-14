from models.application import Application
from sqlalchemy.orm.session import Session
from structlog import get_logger
from validators import app_schema as schemas
from utils.hashing import generate_app_token

logger = get_logger()


async def get_by_id(session: Session, id: int):
    try:
        return session.query(Application).filter(Application.id == id).first()
    except Exception as e:
        logger.exception(f"Exception in get_by_id app query reason {e}")
        return []


async def get_all(session: Session):
    try:
        return session.query(Application).all()
    except Exception as e:
        logger.exception(f"Exception in get_all app query reason {e}")
        return []


async def add(session: Session, app: schemas.CreateApp, user_id: int):
    try:
        token = generate_app_token()
        db_app = Application(
            name=app.name,
            login_url=app.login_url,
            token=token,
            active=True,
            ruler_id=user_id,
        )
        session.add(db_app)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        logger.exception(f"Error in app add dal reason : {e}")
        return False
