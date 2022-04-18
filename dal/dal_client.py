from dal.database import db

def create(client):
    try:
        db.session.add(client)
        db.session.commit()
        return True
    except Exception as e:
        return False