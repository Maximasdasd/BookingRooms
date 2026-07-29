from pydantic import BaseModel, ConfigDict, PositiveInt
from datetime import date


class BookingCreate(BaseModel):
    slot_id: PositiveInt
    booking_date: date


class BookingResponse(BookingCreate):
    model_config = ConfigDict(from_attributes=True)
    staff_id: PositiveInt
    booking_id: PositiveInt