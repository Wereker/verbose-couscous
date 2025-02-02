from sqlalchemy.orm import (
    Mapped, 
    mapped_column,
    relationship,
)

from sqlalchemy import (
    ForeignKey
)

from app.db import Base


class OrderService(Base):
    __tablename__ = "order_service"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id", ondelete="CASCADE"))
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))

    service: Mapped["Service"] = relationship(
        "Service", 
        lazy="joined",
        cascade="all, delete",
    )

    order: Mapped["Order"] = relationship(
        "Order", 
        lazy="joined",
        cascade="all, delete"
    )