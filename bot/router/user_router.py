from aiogram import Router, F
import os
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, WebAppInfo

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from db import requests as rq
from keyboards.keyboards import keyboard as kb

from utils.save_files import get_packages, get_files_names
from utils.test_case import get_test

user = Router()
contests = "C:/Users/gosha/Code_garden/bot/Contests"


class Form(StatesGroup):
    get_test = State()


@user.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user
    await rq.set_user(user.id, user.full_name)
    await message.answer("Привет!\n Что-то надо написать...", reply_markup=await kb.user_keyboard(user.id))


@user.message(F.text == "Назад")
async def cmd_exit(message: Message):
    user = message.from_user
    await message.answer("Вы возвращены домой!", reply_markup=await kb.user_keyboard(user.id))
    

@user.message(F.text == "Получить тест-кейс")
async def cmd_test(message: Message, state: FSMContext):
    text = "Этот бот  отправляет тесты и ответы для задач Соревнования 'Code&Garden' от Яндекс Лицея." \
               "\nВы вводите номер контеста, задачи и теста. Вам придет файл со входными данным и ожидаемым результатом." \
               "\nЗапросы на получение входных данных вы можете делать не чаще, чем раз в 3 минут." \
               "\n<b>====================================</b>" \
               "\n<b>Например</b>" \
               "\nВведите номер контеста (1 для первого по счету проведенного соревнования, 2 второго и т.д), " \
               "\nзатем букву задачи (буква от A до количества задач в этом контесте), а затем номер теста. " \
               "\nНапример '1 C 3' соответствует тесту номер 3 из задачи C первого контеста."

    await message.answer(text, reply_markup=None)
    await state.set_state(Form.get_test)


@user.message(F.text.split(" ").len() == 3, Form.get_test)
async def cmd_test(message: Message, state: FSMContext):
    
    parse = message.text.split(" ")
    parse[1] = parse[1].upper()

    if not os.path.isdir(contests + f"/{parse[0]}"):
        await message.answer("Такого контеста не существует(", reply_markup=await kb.user_keyboard(message.from_user.id))
        await state.clear()
        return
    
    files = await get_files_names(contests + f"/{parse[0]}")

    if parse[1] not in files:
        await message.answer(f"В контесте <b>{parse[0]}</b> не существует такого задания(", reply_markup=await kb.user_keyboard(message.from_user.id))
        await state.clear()
        return
    
    if os.path.isfile(contests + f"/{parse[0]}/{parse[1]}.xls"):
        test = get_test(contests + f"/{parse[0]}/{parse[1]}.xls", parse[2])
    else:
        test = get_test(contests + f"/{parse[0]}/{parse[1]}.xlsx", parse[2])
    
    if test:
        await message.answer(f"""Тест-кейс №{parse[2]} для задания {parse[1]} контеста {parse[0]}:
{test}""", reply_markup=await kb.user_keyboard(message.from_user.id))
        await state.clear()
    else:
        await message.answer(f"В задании №{parse[1]} контеста <b>{parse[0]}</b> не существует такого тест-кейса(", reply_markup=await kb.user_keyboard(message.from_user.id))
        await state.clear()