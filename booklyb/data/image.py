from booklyb.data.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String, Text

import uuid


class Image(Base):
    __tablename__ = "images"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    mime_type: Mapped[str] = mapped_column(String(50))
    image_base64: Mapped[str] = mapped_column(Text)

    book: Mapped["Book"] = relationship(back_populates="image")

    def to_dict(self):
        return {
            "id": self.id,
            "mime_type": self.mime_type,
            "image_base64": self.image_base64
        }
