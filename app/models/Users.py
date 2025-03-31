from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from .Base import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from uuid import UUID,uuid4


class Users(Base):
    __tablename__ = 'users'
    
    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)  
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    audio_files = relationship("AudioFiles", back_populates="user", lazy="selectin")