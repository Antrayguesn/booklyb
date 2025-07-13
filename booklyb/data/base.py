from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session

from booklyb.data.database import engine


class Base(DeclarativeBase):
    def save(self):
        with Session(engine) as session:
            session.add(self)
            session.commit()
