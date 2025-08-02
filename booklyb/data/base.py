from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy import select

from booklyb.data.database import engine


class Base(DeclarativeBase):
    def save(self):
        with Session(engine) as session:
            obj = session.merge(self)
            session.commit()
            session.refresh(obj)
            return obj

    @classmethod
    def find_by_id(cls, id_to_find):
        with Session(engine) as session:
            query = select(cls).filter_by(id=id_to_find)
            result = session.scalars(query)
            return result.first()

    @classmethod
    def find(cls, **kwargs):
        with Session(engine) as session:
            query = select(cls).filter_by(**kwargs)
            result = session.scalars(query)
            return result.unique().all()

    @classmethod
    def execute_query(cls, query):
        with Session(engine) as session:
            result = session.scalars(query)
            return result.unique().all()

    def __repr__(self):
        return repr(self.to_dict())
