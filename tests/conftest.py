import pytest
from bookingroom.core.security import SecurityService
from pwdlib import PasswordHash


@pytest.fixture
def password() -> str:
    return "Maxim123!"

@pytest.fixture
def security_service():
    security_service = SecurityService(
        secret_key="Test_secret_key_QWERTYQWERTYQWERTY",
        algorithm="HS256",
        access_token_expire_minutes=30,
        password_hasher=PasswordHash.recommended()
    )
    return security_service