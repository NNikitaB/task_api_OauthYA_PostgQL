from sqlalchemy import Column, Integer, String
from .Base import Base

class Users(Base):
    __tablename__ = 'users'