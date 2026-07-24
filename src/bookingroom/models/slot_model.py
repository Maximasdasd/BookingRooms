from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint, CheckConstraint, ForeignKey
from bookingroom.models.base import Base
from datetime import time
from typing import List

class Slot(Base):
   __tablename__ = "slot"
   slot_id: Mapped[int] = mapped_column(primary_key=True)
   room_id: Mapped[int] = mapped_column(ForeignKey("room.room_id"), nullable=False)
   start_time: Mapped[time] = mapped_column(nullable=False)
   end_time: Mapped[time] = mapped_column(nullable=False)

   room: Mapped["Room"] = relationship(back_populates="slots")
   bookings: Mapped[List["Booking"]] = relationship(back_populates="slot")

   __table_args__ = (
       CheckConstraint("start_time < end_time", name="ck_slot_time"),
       UniqueConstraint("room_id", "start_time", "end_time", name="uq_slot_for_room"),
    )