from datetime import datetime, timedelta, timezone

import jwt
import pytest

class TestSecurityService:
    def test_verify_password(self, password, security_service):
        result = security_service.hash_password(password)
        assert security_service.verify_password(password, result)
        assert not security_service.verify_password("maxim", result)


    def test_hash_password(self, password, security_service):
        result = security_service.hash_password(password)
        assert isinstance(result, str)
        assert result != password
        assert security_service.verify_password(password, result)


    def test_create_access_token(self, security_service):
        staff_id = 1
        result = security_service.create_access_token(staff_id)
        assert isinstance(result, str)
        assert security_service.decode_access_token(result)['sub'] == str(staff_id)


    def test_decode_access_token(self, security_service):
        staff_id = 1
        token = security_service.create_access_token(staff_id)
        result = security_service.decode_access_token(token)
        now = int(datetime.now(timezone.utc).timestamp())
        assert isinstance(result, dict)
        assert result['sub'] == str(staff_id)
        assert isinstance(result['exp'], int)
        assert result['exp'] - now > 0


    def test_decode_expired_token(self, security_service):
        expired_token = jwt.encode(
            {
                "sub": "1",
                "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
            },
            security_service.secret_key,
            algorithm=security_service.algorithm,
        )

        with pytest.raises(jwt.ExpiredSignatureError):
            security_service.decode_access_token(expired_token)


    def test_decode_token_with_invalid_signature(self, security_service):
        token_with_invalid_signature = jwt.encode(
            {
                "sub": "1",
                "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
            },
            "Another_test_secret_key_QWERTYQWERTY",
            algorithm=security_service.algorithm,
        )

        with pytest.raises(jwt.InvalidSignatureError):
            security_service.decode_access_token(token_with_invalid_signature)
