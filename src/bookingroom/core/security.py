from datetime import datetime, timedelta, timezone

from pwdlib import PasswordHash
import jwt


class SecurityService:
    def __init__(self, 
                 secret_key: str, 
                 algorithm: str, 
                 access_token_expire_minutes: int, 
                 password_hasher: PasswordHash
                ) -> None:

        self.secret_key=secret_key
        self.algorithm=algorithm
        self.access_token_expire_minutes=access_token_expire_minutes
        self.password_hasher=password_hasher

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """проверка хеша с паролем"""
        return self.password_hasher.verify(plain_password, hashed_password)


    def hash_password(self, password: str) -> str:
        """получение хешированного пароля"""
        return self.password_hasher.hash(password)


    def create_access_token(self, staff_id: int) -> str:
        """создание и получение токена jwt"""
        payload = {
            "sub": str(staff_id)
        }
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.access_token_expire_minutes)
        payload.update({"exp": expire})
        encoded_jwt = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt


    def decode_access_token(self, token: str) -> dict:
        """декодирвание токена и получение claim"""
        payload = jwt.decode(
            token, 
            self.secret_key, 
            algorithms=[self.algorithm], 
            options={"require": ["sub", "exp"]}
        )
        return payload