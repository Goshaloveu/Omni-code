from .models import async_session
from .models import User
from sqlalchemy import select, update, delete
from typing import List


async def set_user(tg_id: int, name: str, reiting = 0, post=False, position=0) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, reiting=reiting, name=name, post=post, position=position))
            await session.commit()


async def check_post(tg_id: int) -> bool:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            return bool(user.post)
        else:
            return None
        

async def get_admins() -> List[int]:
    async with async_session() as session:
        admins = await session.scalars(select(User).where(User.post == 1))

        if admins:
            return [admin.tg_id for admin in admins]
        else:
            return None