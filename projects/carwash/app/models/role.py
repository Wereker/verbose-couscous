from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from sqlalchemy import (
    String,
)

from app.db import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))

    role_user: Mapped["RoleUser"] = relationship(
        "RoleUser", 
        back_populates="role",
        cascade="all, delete",
    )
