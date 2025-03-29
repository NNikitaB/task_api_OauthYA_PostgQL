from sqlalchemy import Column, Integer, String
from .Base import Base

class Audio(Base):
    __tablename__ = 'audio'