from fastapi import APIRouter
from bookingroom.services.staff_services import StaffService
from bookingroom.schemas.staff_schema import StaffRegister, StaffResponse
from bookingroom.deps.staff_deps import get_staff_service
from fastapi import Depends
from typing import Annotated

staffrouter = APIRouter()


@staffrouter.post("/register", response_model=StaffResponse, status_code=201)
async def register(staff_data: StaffRegister, staff_service: Annotated[StaffService, Depends(get_staff_service)]) -> StaffResponse:
    return await staff_service.register(staff_data)