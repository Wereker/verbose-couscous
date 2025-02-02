from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from sqlalchemy import (
    DateTime,
    Integer,
    ForeignKey
)

from typing import Optional, List
from datetime import datetime, timezone
from app.db import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[int] = mapped_column(Integer, default=0)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)


    administrator_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    customer_car_id: Mapped[Optional[int]] = mapped_column(ForeignKey("customer_cars.id", ondelete="CASCADE"), nullable=True)
    employee_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=True)

    administrator: Mapped[Optional["User"]] = relationship(
        "User", 
        lazy="joined",
        foreign_keys=[administrator_id],
        back_populates="order_as_administrator",
        cascade="all, delete",
    )

    customer_car: Mapped[Optional["CustomerCars"]] = relationship(
        "CustomerCars", 
        lazy="joined",
        back_populates="order",
        cascade="all, delete",
    )
    
    employee: Mapped[Optional["User"]] = relationship(
        "User", 
        lazy="joined",
        foreign_keys=[employee_id],
        back_populates="order_as_employee",
        cascade="all, delete",
    )

    order_services: Mapped[Optional[List["OrderService"]]] = relationship(
        "OrderService",
        lazy="joined",
        cascade="all, delete",
        overlaps="order",
    )
    