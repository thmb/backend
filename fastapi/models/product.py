'''Product model - SQLAlchemy ORM model.'''
from datetime import datetime
from uuid import UUID

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class Product(Base):
    '''Product model representing a row in the products table.'''

    __tablename__ = 'products'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[datetime] = mapped_column(DateTime, nullable=False)
