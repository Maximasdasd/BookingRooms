from bookingroom.repositories.staff_repositories import StaffRepository
from bookingroom.schemas.staff_schema import StaffRegister, StaffResponse
from bookingroom.core.security import SecurityService
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

class StaffService:
    def __init__(self, staff_repository: StaffRepository, security: SecurityService):
        self.staff_repository = staff_repository
        self.security = security

    async def register(self, staff_data: StaffRegister) -> StaffResponse:
        check_username = await self.staff_repository.get_by_username(staff_data.username)
        if check_username is not None:
            raise HTTPException(status_code=409, detail="такой пользователь существует")
        hash_password = self.security.hash_password(staff_data.password)
        try:
            staff = await self.staff_repository.register(staff_data.username, hash_password)
        except IntegrityError as exc:
            constraint_name = exc.orig.__cause__.constraint_name
            if constraint_name == "uq_staff_username":
                raise HTTPException(status_code=409, detail="такой пользователь существует")
            raise
        return StaffResponse.model_validate(staff)
            
