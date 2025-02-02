from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from sqlalchemy import (
    String,
    Integer,
)

from app.db import Base


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    price: Mapped[int] = mapped_column(Integer)
    time: Mapped[int] = mapped_column(Integer)