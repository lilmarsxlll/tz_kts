from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column


class Base(AsyncAttrs,DeclarativeBase):
    abstract = True
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class Reservation(Base):
    __tablename__ = 'reservations'
    id: Mapped[str] = mapped_column(primary_key=True)
    product_id: Mapped[str] = mapped_column(ForeignKey('products.id'))


class Product(Base):
    __tablename__ = 'products'
    id: Mapped[str] = mapped_column(primary_key=True)
    available_quantity: Mapped[str]
