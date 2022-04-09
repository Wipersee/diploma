from enum import unique
from sqlalchemy import Column, Boolean, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from models.users_application_assoc import UserApplicationAssoc
Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(
        String,
    )
    last_name = Column(String)
    active = Column(Boolean)
    password = Column(String)
    application = relationship('Application', secondary = UserApplicationAssoc, back_populates='user')
