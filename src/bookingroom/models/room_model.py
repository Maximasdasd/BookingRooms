from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint
from bookingroom.models.base import Base
from typing import List



class Room(Base):
    __tablename__ = "room"

    room_id: Mapped[int] = mapped_column(primary_key=True)
    number_room: Mapped[int] = mapped_column(nullable=False)
    office: Mapped[int] = mapped_column(nullable=False)

    slots: Mapped[List["Slot"]] = relationship(back_populates="room")



    __table_args__ = (UniqueConstraint( 'office', 'number_room', name='uq_rooms_office_number'),)
