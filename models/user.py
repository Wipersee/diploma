from enum import unique
from sqlalchemy import Column, Boolean, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from dal.database import db
from datetime import datetime, timedelta


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String, nullable=True)
    email = Column(String)
    last_name = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    password = Column(String)

    def __str__(self):
        return self.username

    def get_user_id(self):
        return self.id


class Token(db.Model):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    expire_at = Column(DateTime, default=datetime.utcnow() + timedelta(days=2))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete="CASCADE"))
    user = db.relationship(User)


class UnauthorizedLogins(db.Model):
    __tablename__ = "unauthorized_logins"

    id = Column(Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete="CASCADE"))
    user = db.relationship(User)
    date = Column(DateTime, default=datetime.utcnow())
    type = Column(String)
    similarity = Column(String)
    photo_filename = Column(String)
