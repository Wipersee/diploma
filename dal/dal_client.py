from dal.database import db
from models.oauth import OAuth2Client


def get(user_id):
    try:
        return db.session.query(OAuth2Client).filter(OAuth2Client.user_id == user_id).all()
    except Exception as e:
        return None


def create(client):
    try:
        db.session.add(client)
        db.session.commit()
        return True
    except Exception as e:
        return False
