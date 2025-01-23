from . import requests as rq
# from typing import List
from aiogram.filters import BaseFilter
from aiogram.types import Message



class IsAdmin(BaseFilter):

    def __init__(self) -> None:
        self.admins_ids = []

    
    async def __call__(self, message: Message) -> bool:
        self.admins_ids = await rq.get_admins()

        if self.admins_ids:
            return message.from_user.id in self.admins_ids
        else:
            return None