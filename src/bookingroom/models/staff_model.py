from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint
from bookingroom.models.base import Base
from typing import List
from enum import Enum

class Role(Enum):
    employee = "employee"
    admin = "admin"


class Staff(Base):
    __tablename__ = "staff"
    staff_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[Role] = mapped_column(nullable=False)

    bookings: Mapped[List['Booking']] = relationship(back_populates="staff")

    __table_args__ = ( 
       UniqueConstraint("username", name="uq_staff_username"),
    )