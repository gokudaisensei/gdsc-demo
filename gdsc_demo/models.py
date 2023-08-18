from sqlalchemy import BigInteger, String, Text, create_engine
from sqlalchemy.orm import (
    as_declarative,
    declared_attr,
    Mapped,
    mapped_column,
    sessionmaker,
)

from typing import Any, Optional

CONNECTION_STRING: str = "sqlite:///setup.db"
ENGINE = create_engine(CONNECTION_STRING)
Session = sessionmaker(ENGINE)
session = Session()


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Product(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[float]
    description: Mapped[str] = mapped_column(Text)


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    hashed_password: Mapped[str]
