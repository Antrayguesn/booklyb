from sqlalchemy import Table, Column, ForeignKey
from booklyb.data.base import Base


author_book_infos_association_table = Table(
    "author_book_infos_association_table",
    Base.metadata,
    Column("book_infos_isbn", ForeignKey("book_infos.id"), primary_key=True),
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
)

publisher_book_infos_association_table = Table(
    "publisher_book_infos_association_table",
    Base.metadata,
    Column("book_infos_isbn", ForeignKey("book_infos.id"), primary_key=True),
    Column("publisher_id", ForeignKey("publishers.id"), primary_key=True),
)
