from bookingroom.repositories.staff_repositories import StaffRepository
from bookingroom.db.database import get_async_session
from bookingroom.core.security import SecurityService
from bookingroom.core.config import settings
from pwdlib import PasswordHash
from bookingroom.services.staff_services import StaffService
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends


def get_staff_repository(
        session: Annotated[AsyncSession, Depends(get_async_session)]
        ) -> StaffRepository:
    return StaffRepository(session)


def get_security_service() -> SecurityService:
    return SecurityService(
        secret_key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
        access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        password_hasher=PasswordHash.recommended(),
    )

def get_staff_service(
        staff_repository: Annotated[StaffRepository, Depends(get_staff_repository)], 
        security: Annotated[SecurityService, Depends(get_security_service)]
)-> StaffService:
    return StaffService(staff_repository, security)