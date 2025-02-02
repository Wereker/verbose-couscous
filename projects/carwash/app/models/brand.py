from sqlalchemy.orm import (
    Mapped, 
    mapped_column,
    relationship
)

from sqlalchemy import (
    String,
)

from app.db import Base


class Brand(Base):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))

    cars: Mapped["Car"] = relationship(
        "Car", 
        back_populates="brand",
        cascade="all, delete",
    )