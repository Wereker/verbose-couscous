from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from sqlalchemy import (
    String,
    ForeignKey,
)

from app.db import Base


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[str] = mapped_column(String(64))
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id", ondelete="CASCADE"))

    brand: Mapped["Brand"] = relationship(
        "Brand", 
        lazy="joined",
        cascade="all, delete",
    )

    customer_cars: Mapped["CustomerCars"] = relationship(
        "CustomerCars", 
        back_populates="car",
        cascade="all, delete",
    )