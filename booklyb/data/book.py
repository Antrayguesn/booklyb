from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

import uuid

from booklyb.data.base import Base


class Book(Base):
    __tablename__ = "books"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    isbn: Mapped[str] = mapped_column(String(13))
    book_info_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("book_infos.id"), nullable=True)

    book_info: Mapped["BookInfo"] = relationship(
        back_populates="books"
    )
