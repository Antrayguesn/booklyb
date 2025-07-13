import uuid
from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from booklyb.data.base import Base
from booklyb.data.association_table import publisher_book_infos_association_table


class Publisher(Base):
    __tablename__ = "publishers"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(150))

    book_infos: Mapped[List["BookInfo"]] = relationship(
        secondary=publisher_book_infos_association_table, back_populates="publishers"
    )
