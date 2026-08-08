import pytest
import pytest_asyncio
from bookingroom.core.security import SecurityService
from unittest.mock import AsyncMock, Mock
from pwdlib import PasswordHash
from bookingroom.repositories.staff_repositories import StaffRepository
from bookingroom.services.staff_services import StaffService
from httpx2 import ASGITransport, AsyncClient
from bookingroom.main import app
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from bookingroom.core.config import settings
from bookingroom.models.staff_model import Staff
from bookingroom.models.booking_model import Booking
from sqlalchemy import delete
from bookingroom.db.database import get_async_session
from sqlalchemy.pool import NullPool



engine_test = create_async_engine(settings.TEST_DATABASE_URL, echo=True, poolclass=NullPool)

async_session_maker_test = async_sessionmaker(
    engine_test, 
    expire_on_commit=False,
    )

async def get_async_session_test():
    """генератор сессий для ендпоинтов"""
    async with async_session_maker_test() as async_session_test:
        yield async_session_test



@pytest_asyncio.fixture
async def clean_database():
    async with async_session_maker_test() as async_session_test:
        await async_session_test.execute(delete(Booking))
        await async_session_test.execute(delete(Staff))
        await async_session_test.commit()
        yield
        await async_session_test.execute(delete(Booking))
        await async_session_test.execute(delete(Staff))
        await async_session_test.commit()


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        app.dependency_overrides[get_async_session] = get_async_session_test
        yield ac
        app.dependency_overrides.pop(get_async_session, None)


@pytest.fixture
def password() -> str:
    return "Maxim123!"


@pytest.fixture
def security_service() -> SecurityService:
    security_service = SecurityService(
        secret_key="Test_secret_key_QWERTYQWERTYQWERTY",
        algorithm="HS256",
        access_token_expire_minutes=30,
        password_hasher=PasswordHash.recommended()
    )
    return security_service


@pytest.fixture
def staff_service():
    repository = Mock(spec=StaffRepository)
    repository.get_by_username = AsyncMock()
    repository.register = AsyncMock()

    security = Mock(spec=SecurityService)
    service = StaffService(repository, security)

    return service, repository, security