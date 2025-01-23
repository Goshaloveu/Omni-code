from aiogram import Router, F
import asyncio
import aiofiles
import os
import shutil
from pathlib import Path
from itertools import islice
from bot import bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from utils.save_files import extr_files, get_files, get_packages, get_files_names, struct

import db.requests as rq
from db.admins import IsAdmin

from keyboards.keyboards import keyboard as kb
from aiogram.utils.chat_action import ChatActionSender

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    add_contest = State()
    contest_arch = State()

    del_contest = State()

    add_ex_name = State()
    add_ex_file = State()

    tran_ex = State()

    del_ex_name = State()
    del_ex_let = State()
    del_ex_try = State()

    check_contest = State()


content = Router()
dest = "C:/Users/gosha/Code_garden/bot/temp"
contests = "C:/Users/gosha/Code_garden/bot/Contests"
mime_archs = {"application/zip", "application/x-zip-compressed", # -  Zip
              "application/x-7z-compressed", # -  7Zip
              "application/vnd.rar"} # -  Rar
mime_excel = {'application/vnd.ms-excel', 
              'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}


@content.message((F.text == "Просмотр контестов"), IsAdmin())
async def cmd_check_contests(message: Message, state: FSMContext):
    
    dirs = await get_packages(contests)
    text = ""
    folder = Path(r'C:\Users\gosha\Code_garden\bot\Contests')
    iterator = struct(folder)
    for line in islice(iterator, 500):
        text += line + "\n"
        print(line)

    await message.answer(text, reply_markup=kb.create_inline_table(dirs))
    await state.set_state(Form.check_contest)


@content.message((F.text == "Добавить контест"), IsAdmin())
async def cmd_add_contest(message: Message, state: FSMContext):

    await message.answer("Отправь мне название контеста", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.add_contest)


@content.message(F.text, Form.add_contest, IsAdmin())
async def cmd_add_contest(message: Message, state: FSMContext):
    await state.update_data(name_contest=message.text)
    
    await message.answer("""А теперь отправь мне <i>архив с файлами-заданиями</i>:
<b>Расширение файла</b> должно быть <b>.xls (.xlsx)</b> 
каждая <b>строка</b> в котором будет означать <b>тест-кейс</b>, 
а <b>первый и второй столбец - входные данные и результат</b> соответственно.
                             
В случае нарушения одного из условий я могу работать некорректно((((""")

    await state.set_state(Form.contest_arch)


@content.message(F.document.mime_type.in_(mime_archs), Form.contest_arch, IsAdmin())
async def cmd_add_contest(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name_contest")
    archive_path = dest + f"/{message.document.file_name}"

    await bot.download(file=message.document.file_id, destination=archive_path)

    result = await extr_files(path=contests + f"/{name}", archive_path=archive_path)
    os.remove(archive_path)

    await message.answer(f"all ok", reply_markup=await kb.user_keyboard(message.from_user.id))
    await state.clear()


@content.message((F.text == "Удалить контест"), IsAdmin())
async def cmd_del_contest(message: Message, state: FSMContext):

    dirs = await get_packages(contests)
    await message.answer("Выберите контест для удаления", reply_markup=kb.create_inline_table(dirs))

    await state.set_state(Form.del_contest)


@content.callback_query(F.data, Form.del_contest, IsAdmin())
async def cmd_del_contest_call(call: CallbackQuery, state:FSMContext):

    shutil.rmtree(f"{contests}/{call.data}")
    await call.message.edit_text(f"Контест <b>{call.data}</b> успешно удален!", reply_markup=None)
    await state.clear()


@content.message(F.text == "Добавить задание", IsAdmin())
async def cmd_add_ex(message: Message, state: FSMContext):

    dirs = await get_packages(contests)

    if dirs:
        await message.answer("Выберите в какой контест вы хотите добавить задание...", reply_markup=kb.create_inline_table(dirs))

        await state.set_state(Form.add_ex_name)

    else:
        await message.answer("""В данный момент имеется 0 контестов...
- Нажмите на кнопку <b>"Добавить контест"</b> если вы хотите добавить новый контест""", reply_markup=kb.content())


@content.callback_query(F.data, Form.add_ex_name, IsAdmin())
async def cmd_add_ex_call(call: CallbackQuery, state:FSMContext):
    await state.update_data(contest=call.data)
    
    await call.message.edit_text("""Отправьте <i>файл с тест-кейсами</i>:
<b>Расширение файла</b> должно быть <b>.xls (.xlsx)</b> 
каждая <b>строка</b> в котором будет означать <b>тест-кейс</b>, 
а <b>первый и второй столбец - входные данные и результат</b> соответственно.
                             
В случае нарушения одного из условий я могу работать некорректно((((""", reply_markup=None)
    
    await state.set_state(Form.add_ex_file)


@content.message(F.document.mime_type.in_(mime_excel), Form.add_ex_file, IsAdmin())
async def cmd_del_contest(message: Message, state:FSMContext):
    data = await state.get_data()
    name = data.get("contest")
    contest_path = contests + f"/{name}"

    await bot.download(file=message.document.file_id, destination=contest_path + f"/{message.document.file_name}")
    
    await message.answer(f"Задание <b>{message.document.file_name.split('.')[0]}</b> успешно добавлено в <b>{name}</b>", reply_markup=kb.content())
    await state.clear()


@content.message((F.text == "Изменить задание"), IsAdmin())
async def cmd_transfrom_ex(message: Message, state: FSMContext):
    await message.answer("Извините в данный момент эта кнопка не работает((((")


@content.message((F.text == "Удалить задание"), IsAdmin())
async def cmd_del_ex(message: Message, state: FSMContext):

    dirs = await get_packages(contests)

    if dirs:
        await message.answer("Выберите из какого контеста вы хотите удалить задание...", reply_markup=kb.create_inline_table(dirs))

        await state.set_state(Form.del_ex_name)

    else:
        await message.answer("""В данный момент имеется 0 контестов...
- Нажмите на кнопку <b>"Добавить контест"</b> если вы хотите добавить новый контест""", reply_markup=kb.content())


@content.callback_query(F.data, Form.del_ex_name, IsAdmin())
async def cmd_add_ex_call(call: CallbackQuery, state:FSMContext):
    await state.update_data(contest=call.data)
    
    await call.message.edit_text("Теперь отправьте мне букву задания", reply_markup=None)
    
    await state.set_state(Form.del_ex_let)


@content.message(F.text, Form.del_ex_let, IsAdmin())
async def cmd_del_ex_mes(message: Message, state:FSMContext):
    data = await state.get_data()
    name = data.get("contest")
    contest_path = contests + f"/{name}"
    
    files = await get_files_names(contest_path)
    ex = message.text.upper()

    if ex in files:
        try:
            os.remove(contest_path + f"/{ex}.xls")
        except:
            os.remove(contest_path + f"/{ex}.xlsx")
        await message.answer(f"Задание <b>{ex}</b> успешно удалено в <b>{name}</b>", reply_markup=kb.content())
        await state.clear()
    else:
        await message.answer(f"""Задание <b>{ex}</b> не существует в контесте <b>{name}</b>
Попробуйте ввести букву задания снова""", reply_markup=kb.create_inline_table(["Выход", "Ввести заново"], 1))
        await state.set_state(Form.del_ex_try)


@content.callback_query(F.data, Form.del_ex_try, IsAdmin())
async def cmd_del_ex_try(call: CallbackQuery, state:FSMContext):
    
    if call.data == "Ввести заново":
        await call.message.edit_text("Теперь отправьте мне букву задания", reply_markup=None)
        
        await state.set_state(Form.del_ex_let)
    else:
        await call.message.edit_text("Вы возвращены назад", reply_markup=kb.contest())
        
        await state.clear()