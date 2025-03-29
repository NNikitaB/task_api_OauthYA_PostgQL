from sqlalchemy import Column, Integer, String, ForeignKey
from .Base import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from uuid import UUID


class AudioFiles(Base):
    __tablename__ = "audio_files"

    id: Mapped[Integer] = mapped_column(primary_key=True)
    user_uuid: Mapped[UUID] = mapped_column(ForeignKey("users.uuid"), nullable=False)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)

    user = relationship("Users", back_populates="audio_files")