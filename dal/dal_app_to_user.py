from models.app_to_user import UserApplicationRecord
from sqlalchemy.orm.session import Session
from structlog import get_logger

logger = get_logger()


async def get_by_ids(session: Session, user_id: int, app_id: int):
    try:
        return session.query(UserApplicationRecord).filter(
            UserApplicationRecord.user_id == user_id,
            UserApplicationRecord.application_id == app_id,
        )
    except Exception as e:
        logger.excepct(f"Exception in user_to_app get_by_ids reason {e}")
        return None
