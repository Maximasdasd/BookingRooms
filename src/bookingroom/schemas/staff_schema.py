from pydantic import BaseModel, PositiveInt, ConfigDict, Field, field_validator
from bookingroom.models.staff_model import Role


class StaffLogin(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)


class StaffRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)

    @field_validator('password', mode='after')
    @classmethod
    def password_check(cls, value: str) -> str:
        symbol = '!@#$%^&*()'
        has_spec = any(char in symbol for char in value)
        if not has_spec:
            raise ValueError("Пароль должен содержать спецсимволы")
        return value


class StaffResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    staff_id: PositiveInt
    username: str
    role: Role