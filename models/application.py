from sqlalchemy import Column, Boolean, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy.orm import relationship
from models.users_application_assoc import UserApplicationAssoc

Base = declarative_base()


class Application(Base):
    __tablename__ = "application"

    app_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    login_url = Column(String)
    token = Column(String)
    active = Column(Boolean)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship('User', secondary = UserApplicationAssoc, back_populates='application')