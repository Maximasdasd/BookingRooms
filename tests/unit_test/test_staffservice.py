import pytest
from unittest.mock import AsyncMock, Mock

from bookingroom.core.security import SecurityService
from bookingroom.models.staff_model import Role, Staff
from bookingroom.repositories.staff_repositories import StaffRepository
from bookingroom.schemas.staff_schema import StaffRegister
from bookingroom.services.staff_services import StaffService
from fastapi import HTTPException

@pytest.mark.asyncio
async def test_register_creates_staff():
    staff_data = StaffRegister(
        username="maxim",
        password="Password123!",
    )

    created_staff = Staff(
        staff_id=1,
        username="maxim",
        password_hash="fake_hash",
        role=Role.employee,
    )

    repository = Mock(spec=StaffRepository)
    repository.get_by_username = AsyncMock(return_value=None)
    repository.register = AsyncMock(return_value=created_staff)

    security = Mock(spec=SecurityService)
    security.hash_password.return_value = "fake_hash"

    service = StaffService(
        staff_repository=repository,
        security=security,
    )

    result = await service.register(staff_data)

    assert result.staff_id == 1
    assert result.username == "maxim"
    assert result.role == Role.employee

    security.hash_password.assert_called_once_with(
        "Password123!",
    )

    repository.register.assert_awaited_once_with(
        "maxim",
        "fake_hash",
    )

@pytest.mark.asyncio
async def test_register_already_exists(staff_service):
    existing_staff = Staff(
        staff_id=1,
        username="maxim",
        password_hash="hash",
        role=Role.employee,
    )

    service, repository, security = staff_service
    repository.get_by_username.return_value = existing_staff
    with pytest.raises(HTTPException) as exc_info:
        await service.register(
            StaffRegister(
                username="maxim",
                password="Password123!",
            )
        )

    assert exc_info.value.status_code == 409
    security.hash_password.assert_not_called()
    repository.register.assert_not_awaited()
