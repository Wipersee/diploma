# from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
# from models.user import User
# from models.application import Application
# import datetime

# Base = declarative_base()


# class UserApplicationRecord(Base):
#     __tablename__ = "user_application_record"

#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey(User.id))
#     application_id = Column(Integer, ForeignKey(Application.id))
#     created_at = Column(DateTime, default=datetime.datetime.utcnow)
#     active = Column(Boolean, default=True)
