from typing import List
import uuid

from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from booklyb.data.base import Base
from booklyb.data.book import Book
from booklyb.data.author import Author
from booklyb.data.publisher import Publisher

from booklyb.data.association_table import author_book_infos_association_table
from booklyb.data.association_table import publisher_book_infos_association_table

from booklyb.data.log import log, WARNING_MORE_THAN_ONE_RESULT_RETURNED

from datetime import datetime


MSG_WRN_MORE_THAN_ONE_RESULT_RETURNED = "Execpted one result but {} returned, first id take {} for procesing"


class BookInfo(Base):
    __tablename__ = "book_infos"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    isbn: Mapped[str] = mapped_column(String(13))
    title: Mapped[str] = mapped_column(String(150), nullable=True)
    subtitle: Mapped[str] = mapped_column(String(150), nullable=True)
    fetcher_name: Mapped[str] = mapped_column(String(150), nullable=True)
    volume_number: Mapped[int] = mapped_column(Integer(), nullable=True)

    authors: Mapped[List[Author]] = relationship(
        secondary=author_book_infos_association_table,
        back_populates="book_infos",
        lazy="joined"
    )

    publishers: Mapped[List[Publisher]] = relationship(
        secondary=publisher_book_infos_association_table,
        back_populates="book_infos",
        lazy="joined"
    )

    published_date: Mapped[int] = mapped_column(Integer(), nullable=True)
    page_count: Mapped[int] = mapped_column(Integer(), nullable=True)

    height_mm: Mapped[int] = mapped_column(Integer(), nullable=True)
    width_mm: Mapped[int] = mapped_column(Integer(), nullable=True)
    thickness_mm: Mapped[int] = mapped_column(Integer(), nullable=True)

    target_audience: Mapped[str] = mapped_column(String(50), nullable=True)
    language: Mapped[str] = mapped_column(String(50), nullable=True)
    description: Mapped[str] = mapped_column(String(300), nullable=True)

    serie: Mapped[str] = mapped_column(String(100), nullable=True)

    created_time: Mapped[int] = mapped_column(Integer(), nullable=True, default=datetime.now())
    modified_time: Mapped[int] = mapped_column(Integer(), nullable=True, default=datetime.now())

    books: Mapped[list["Book"]] = relationship(
        back_populates="book_info"
    )

    # fetcher_request_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("fetcher_requests.id"), nullable=True)

    # fetcher_request: Mapped["FetcherRequest"] = relationship(back_populates="book_info")

    def add_authors(self, authors_name: list):
        authors = []
        for author_name in authors_name:
            authors_in_database = Author.find(name=author_name)
            if len(authors_in_database) >= 1:
                if len(authors_in_database) > 1:
                    log(code=WARNING_MORE_THAN_ONE_RESULT_RETURNED,
                        msg=MSG_WRN_MORE_THAN_ONE_RESULT_RETURNED.format(len(authors_in_database), authors_in_database[0].id),
                        authors=[str(a.id) for a in authors_in_database])
                authors.append(authors_in_database[0])
            else:
                # We first need to save the author in database to create the ID
                # end return it
                author = Author(name=author_name)
                authors.append(author)
        self.authors = authors

    def add_publisher(self, publisher_name):
        publishers = []
        if publisher_name:
            publishers_in_database = Publisher.find(name=publisher_name)
            if len(publishers_in_database) >= 1:
                if len(publishers_in_database) > 1:
                    log(code=WARNING_MORE_THAN_ONE_RESULT_RETURNED,
                        msg=MSG_WRN_MORE_THAN_ONE_RESULT_RETURNED.format(len(publishers_in_database), publishers_in_database[0].id),
                        publishers=[str(a.id) for a in publishers_in_database])
                publishers.append(publishers_in_database[0])
            else:
                publisher = Publisher(name=publisher_name)
                publishers.append(publisher)
        self.publishers = publishers

    def to_dict(self):
        return {
            "id": str(self.id),
            "isbn": self.isbn,
            "serie": self.serie,
            "title": self.title,
            "subtitle": self.subtitle,
            "volume_number": self.volume_number,
            "authors": [str(a.id) for a in self.authors],
            "publishers": [str(p.id) for p in self.publishers],
            "published_date": self.published_date,
            "page_count": self.page_count,
            "height_mm": self.height_mm,
            "width_mm": self.width_mm,
            "thickness_mm": self.thickness_mm,
            "target_audience": self.target_audience,
            "language": self.language,
            "description": self.description,
            "created_time": self.created_time,
            "modified_date": self.modified_time
        }
