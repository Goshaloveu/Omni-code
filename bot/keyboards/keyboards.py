from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List
from db import requests as rq


web = WebAppInfo(url="https://www.youtube.com/watch?v=1njlwbOw6B0&list=PL0lO_mIqDDFVfIjOW2NsBaDYXB_ZwDB0p&index=13")



class keyboard():
    
    async def user_keyboard(tg_id: int):

        keyboard=[
            [KeyboardButton(text="Мой профиль")],
            [KeyboardButton(text="Рейтинг", web_app=web), KeyboardButton(text="Получить тест-кейс")]
        ]
        
        
        if await rq.check_post(tg_id):
            keyboard.append([KeyboardButton(text="Admin Panel")])

        return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню...")


    def admin_panel():

        keyboard = [
            [KeyboardButton(text="Пользователи")], 
            [KeyboardButton(text="Контент"), KeyboardButton(text="База данных")],
            [KeyboardButton(text="Назад")]
        ]

        return ReplyKeyboardMarkup(keyboard=keyboard,resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню...")


    def content():

        keyboard=[
            [KeyboardButton(text="Добавить контест"), KeyboardButton(text="Просмотр контестов"), KeyboardButton(text="Удалить контест")],
            [KeyboardButton(text="Добавить задание"), KeyboardButton(text="Изменить задание"), KeyboardButton(text="Удалить задание")],
            [KeyboardButton(text="Назад")]
        ]

        return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню...")
    
    
    def users():

        keyboard=[
            [KeyboardButton(text="Пока что ничего...")],
            [KeyboardButton(text="Назад")]
        ]

        return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню...")
    

    def data():

        keyboard=[
            [KeyboardButton(text="Пока что ничего...")],
            ["Назад"]
        ]

        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню...")
    
    def create_inline_table(dirs: List, columns: int = 2) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        for dir in dirs:
            builder.button(text=dir, callback_data=dir)
        
        return builder.adjust(columns).as_markup()