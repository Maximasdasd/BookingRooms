from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint, ForeignKey
from bookingroom.models.base import Base
from datetime import date

class Booking(Base):
   __tablename__ = "booking"
   booking_id: Mapped[int] = mapped_column(primary_key=True)
   staff_id: Mapped[int] = mapped_column(ForeignKey("staff.staff_id"), nullable=False, index=True)
   slot_id: Mapped[int] = mapped_column(ForeignKey("slot.slot_id"), nullable=False)
   booking_date: Mapped[date] = mapped_column(nullable=False)

   staff: Mapped["Staff"] = relationship(back_populates="bookings")
   slot: Mapped["Slot"] = relationship(back_populates="bookings")

   __table_args__ = ( 
       UniqueConstraint("booking_date", "slot_id", name="uq_booking_date_slot"),
    )
