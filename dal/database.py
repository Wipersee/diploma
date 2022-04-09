from config.settings import DATABASE_URL

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)


def get_session():
    session = Session()
    try:
        yield session
    except:
        raise
    finally:
        session.close
