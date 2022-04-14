from sqlalchemy import Column, Boolean, String, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy.orm import relationship
from models.user import User

Base = declarative_base()


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    login_url = Column(String)
    token = Column(String)
    active = Column(Boolean)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    ruler_id = Column(Integer, ForeignKey(User.id))
