from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from sqlalchemy import (
    String,
    Boolean,
)

from typing import List, Optional
from app.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(64), nullable=True)
    last_name: Mapped[str] = mapped_column(String(64), nullable=True)
    patronymic: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_send_notify: Mapped[Optional[bool]] = mapped_column(Boolean, default=False, nullable=True)

    role_user: Mapped[Optional["RoleUser"]] = relationship(
        "RoleUser", 
        back_populates="user",
        lazy="selectin"
    )
    
    customer_cars: Mapped[List["CustomerCars"]] = relationship(
        "CustomerCars", 
        back_populates="customer",
        lazy="selectin"
    )

    order_as_administrator: Mapped[List["Order"]] = relationship(
        "Order",
        back_populates="administrator",
        lazy="selectin",
        foreign_keys="Order.administrator_id"
    )
    
    order_as_employee: Mapped[List["Order"]] = relationship(
        "Order",
        back_populates="employee",
        lazy="selectin",
        foreign_keys="Order.employee_id"
    )

    @property
    def full_name(self):
        """Склеиваем ФИО в одну строку."""
        return f"{self.last_name} {self.first_name} {self.patronymic if self.patronymic else ''}".strip()
    
