from __future__ import annotations

import logging
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from flask_app.models.base import Base

log = logging.getLogger(__name__)


class Books_Issued(Base):
    __tablename__: str = "books_issued"

    id: Column = Column(Integer, primary_key=True)
    member_no: Column = Column(String(50), nullable=False)
    book_title: Column = Column(String(100), nullable=False)
    author: Column = Column(String(50), nullable=False)
    issue_date:Column= Column(DateTime(timezone=False), nullable=False)
    return_date:Column= Column(DateTime(timezone=False), nullable=False)