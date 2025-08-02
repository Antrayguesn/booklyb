from datetime import datetime
import uuid

from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Integer

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from booklyb.data.base import Base


class FetcherRequest(Base):
    __tablename__ = "fetcher_requests"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    fetcher_name: Mapped[str] = mapped_column(String(100))
    url: Mapped[str] = mapped_column(String(300))
    timestamp: Mapped[int] = mapped_column(Integer(), nullable=True, default=datetime.now())
    status_code: Mapped[int] = mapped_column(Integer(), nullable=True)

    request_content: Mapped[str] = mapped_column(Text(), nullable=True)
