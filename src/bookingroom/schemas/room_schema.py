from pydantic import BaseModel, PositiveInt, ConfigDict


class RoomCreate(BaseModel):
    number_room: PositiveInt
    office: PositiveInt


class RoomResponse(RoomCreate):
    model_config = ConfigDict(from_attributes=True)
    room_id: int