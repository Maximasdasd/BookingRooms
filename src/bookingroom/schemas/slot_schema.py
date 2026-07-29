from pydantic import BaseModel, ConfigDict, model_validator, PositiveInt
from typing import Self
from datetime import time


class SlotCreate(BaseModel):
    room_id: PositiveInt
    start_time: time
    end_time: time

    @model_validator(mode='after')
    def check_start_end_time(self) -> Self:
        if self.start_time < self.end_time:
            return self
        else:
            raise ValueError('Время начало слота должно быть меньше чем конец слота')


class SlotResponse(SlotCreate):
    model_config = ConfigDict(from_attributes=True)
    slot_id: PositiveInt