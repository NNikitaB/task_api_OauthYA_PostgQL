from sqlalchemy import Column, Integer, String, ForeignKey
from .Base import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from uuid import UUID


class AudioFiles(Base):
    __tablename__ = "audio_files"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_uuid: Mapped[UUID] = mapped_column(ForeignKey("users.uuid"), nullable=False)
    file_name: Mapped[str] = mapped_column(nullable=False)
    file_path: Mapped[str] = mapped_column(nullable=False)

    user = relationship("Users", back_populates="audio_files", lazy="selectin")