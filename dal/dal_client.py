from dal.database import db
from models.oauth import OAuth2Client, OAuth2AuthorizationCode, OAuth2Token
from structlog import get_logger

logger = get_logger()

def get(user_id):
    try:
        return (
            db.session.query(OAuth2Client).filter(OAuth2Client.user_id == user_id).all()
        )
    except Exception as e:
        logger.exception(f"Exception occured in get client. Reason : {e}")
        return None


def get_by_id(client_id):
    try:
        return (
            db.session.query(OAuth2Client).filter(OAuth2Client.id == client_id).first()
        )
    except Exception as e:
        logger.exception(f"Exception occured in get_by_id. Reason : {e}")
        return None


def get_grant_access(user_id):
    try:
        return (
            db.session.query(OAuth2Token, OAuth2Client)
            .filter(OAuth2Token.user_id == user_id)
            .join(OAuth2Client, OAuth2Token.client_id == OAuth2Client.client_id)
            .all()
        )
    except Exception as e:
        logger.exception(f"Exception occured in get_grant_access. Reason : {e}")
        return None


def get_grant_access_one(user_id, access_id):
    try:
        return (
            db.session.query(OAuth2Token)
            .filter(OAuth2Token.user_id == user_id, OAuth2Token.id == access_id)
            .first()
        )
    except Exception as e:
        logger.exception(f"Exception occured in get_grant_access_one. Reason : {e}")
        return None


def revoke_grant_access(access_id):
    try:
        obj = db.session.query(OAuth2Token).filter(OAuth2Token.id == access_id).first()
        if obj:
            db.session.delete(obj)
            db.session.commit()
        return True
    except Exception as e:
        logger.exception(f"Exception occured in revoke_grant_access. Reason : {e}")
        return None


def create(client):
    try:
        db.session.add(client)
        db.session.commit()
        return True
    except Exception as e:
        logger.exception(f"Exception occured in create client. Reason : {e}")
        return False


def delete_oauth_code(client_id):
    try:
        obj = (
            db.session.query(OAuth2AuthorizationCode)
            .filter(OAuth2AuthorizationCode.client_id == client_id)
            .all()
        )
        if obj:
            for o in obj:
                db.session.delete(o)
            db.session.commit()
        return True
    except Exception as e:
        logger.exception(f"Exception occured in delete_oauth_code. Reason : {e}")
        return None


def delete_oauth_token(client_id):
    try:
        obj = (
            db.session.query(OAuth2Token)
            .filter(OAuth2Token.client_id == client_id)
            .all()
        )
        if obj:
            for o in obj:
                db.session.delete(o)
            db.session.commit()
        return True
    except Exception as e:
        logger.exception(f"Exception occured in delete_oauth_token. Reason : {e}")
        return None


def delete_oauth_client(client_id):
    try:
        obj = (
            db.session.query(OAuth2Client)
            .filter(OAuth2Client.client_id == client_id)
            .first()
        )
        db.session.delete(obj)
        db.session.commit()
        return True
    except Exception as e:
        logger.exception(f"Exception occured in delete_oauth_client. Reason : {e}")
        return None
