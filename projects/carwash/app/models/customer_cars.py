from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
)

from app.db import Base


class CustomerCars(Base):
    __tablename__ = "customer_cars"

    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(Integer)
    number: Mapped[str] = mapped_column(String(16))

    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id", ondelete="CASCADE"))
    customer_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    car: Mapped["Car"] = relationship(
        "Car", 
        lazy="joined",
        cascade="all, delete",
    )

    customer: Mapped["User"] = relationship(
        "User", 
        lazy="joined",
        cascade="all, delete",
    )

    order: Mapped["Order"] = relationship(
        "Order", 
        back_populates="customer_car",
        cascade="all, delete",
    )