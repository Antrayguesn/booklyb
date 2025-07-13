from typing import List
from datetime import date
import uuid

from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import Integer

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from booklyb.data.base import Base
from booklyb.data.book import Book
from booklyb.data.author import Author
from booklyb.data.publisher import Publisher

from booklyb.data.association_table import author_book_infos_association_table
from booklyb.data.association_table import publisher_book_infos_association_table


class BookInfo(Base):
    __tablename__ = "book_infos"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    isbn: Mapped[str] = mapped_column(String(13))
    title: Mapped[str] = mapped_column(String(150), nullable=True)

    authors: Mapped[List[Author]] = relationship(
        secondary=author_book_infos_association_table, back_populates="book_infos"
    )

    publishers: Mapped[List[Publisher]] = relationship(
        secondary=publisher_book_infos_association_table, back_populates="book_infos"
    )

    published_date: Mapped[date] = mapped_column(Date(), nullable=True)
    page_count: Mapped[int] = mapped_column(Integer(), nullable=True)
    dimensions = {}
    maturity_rating: Mapped[str] = mapped_column(String(50), nullable=True)
    language: Mapped[str] = mapped_column(String(50), nullable=True)
    books: Mapped[list["Book"]] = relationship(
        back_populates="book_info"
    )
