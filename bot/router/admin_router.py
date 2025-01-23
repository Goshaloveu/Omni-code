from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, WebAppInfo
import db.requests as rq
from keyboards.keyboards import keyboard as kb
from db.admins import IsAdmin

admin = Router()



@admin.message((F.text == "Admin Panel"), IsAdmin())
async def cmd_admin(message: Message):
    user = message.from_user
    await message.answer(f"Привет {user.username}!", reply_markup=kb.admin_panel())


@admin.message((F.text == "Пользователи"), IsAdmin())
async def cmd_users(message: Message):
    user = message.from_user
    await message.answer(f"Привет {user.first_name}!", reply_markup=kb.users())


@admin.message((F.text == "База данных"), IsAdmin())
async def cmd_db(message: Message):
    user = message.from_user
    await message.answer(f"Привет {user.first_name}!", reply_markup=kb.data())


@admin.message((F.text == "Контент"), IsAdmin())
async def cmd_content(message: Message):
    user = message.from_user
    await message.answer(f"Привет {user.first_name}!", reply_markup=kb.content())


