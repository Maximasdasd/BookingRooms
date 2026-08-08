from bookingroom.models.staff_model import Staff, Role
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class StaffRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_by_username(self, username: str) -> Staff | None:
        stmt = select(Staff).where(Staff.username == username)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()


    async def register(self, username: str, password_hash: str) -> Staff:
        staff = Staff(username=username, password_hash=password_hash, role=Role.employee)
        try:
            self.session.add(staff)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
        return staff