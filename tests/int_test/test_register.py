import pytest
from httpx2 import AsyncClient
from tests.conftest import async_session_maker_test
from sqlalchemy import select
from bookingroom.models.staff_model import Staff, Role
from sqlalchemy.exc import IntegrityError


@pytest.mark.asyncio
async def test_register_positive(async_client: AsyncClient, clean_database):

        result = await async_client.post("/register", json={"username": "Maxim123",
                                                            "password": "Maxim123!"})
        
        async with async_session_maker_test() as async_session_test:
                usernameIsNone = await async_session_test.execute(select(Staff).where(Staff.username=="Maxim123"))
                staff = usernameIsNone.scalar_one_or_none()
                assert staff is not None
                assert result.status_code == 201
                response_data = result.json()
                assert "password_hash" not in response_data
                assert "username" in response_data
                assert "staff_id" in response_data
                assert "role" in response_data
                check_password = await async_session_test.execute(select(Staff.password_hash).where(Staff.username=="Maxim123"))
                password = check_password.scalar_one_or_none()
                assert password != "Maxim123!"

@pytest.mark.asyncio
async def test_register_already_exists(async_client: AsyncClient, clean_database):
        beforeresult = await async_client.post("/register", json={"username": "Maxim123",
                                                            "password": "Maxim123!"})
        assert beforeresult.status_code == 201
        
        result = await async_client.post("/register", json={"username": "Maxim123",
                                                        "password": "Maxim123!"})
        assert result.status_code == 409

@pytest.mark.asyncio
async def test_register_rejects_invalid_password(async_client: AsyncClient, clean_database):
        result_password = await async_client.post("/register", json={"username": "Maxim123",
                                                        "password": "Maxim123"})

        assert result_password.status_code == 422
        async with async_session_maker_test() as async_session_test:
                usernameIsNone = await async_session_test.execute(select(Staff).where(Staff.username=="Maxim123"))
                staff = usernameIsNone.scalar_one_or_none()
                assert staff is None

@pytest.mark.asyncio
async def test_register_rejects_missing_fields(async_client: AsyncClient, clean_database):
        result = await async_client.post("/register", json={})
        assert result.status_code == 422

@pytest.mark.asyncio
async def test_staff_username_unique_constraint(clean_database):
        async with async_session_maker_test() as session:
                session.add(
                        Staff(
                        username="Maxim123",
                        password_hash="fake_hash",
                        role=Role.employee,
                        )
                )
                await session.commit()

                session.add(
                        Staff(
                        username="Maxim123",
                        password_hash="another_hash",
                        role=Role.employee,
                        )
                )

                with pytest.raises(IntegrityError) as exc:
                        await session.commit()
                await session.rollback()

        postgres_error = exc.value.orig.__cause__
        assert postgres_error.constraint_name == "uq_staff_username"