from email import message
from re import X
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import keyboard
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import logging

router = Router()

class Lis(StatesGroup):
    list = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Hello, I'm a shopping list bot.\n If you need create a new list or edit existing, use button bellow \n For other information use /help",
                      reply_markup=kb.main)

@router.message(F.text == "New list")
async def list_one(message: Message, state: FSMContext):
    await state.set_state(Lis.list)
    await message.answer("Write your products separating by paragraphs")

@router.message(Lis.list)
async def list_two(message: Message, state: FSMContext):
    await state.update_data(list=message.text)
    data = await state.get_data()   
    products = data["list"].splitlines()
    inline_kb = await kb.inline_list(products)
    await message.answer("Your list", reply_markup=inline_kb)
    await state.clear()

@router.callback_query(F.data.startswith("del_"))
async def delit(callback : CallbackQuery):
     current_list = callback.message.reply_markup.inline_keyboard

     pressed_button_info = callback.data.split('_')
     edit_row_number = int(pressed_button_info[1])

     del current_list[edit_row_number - 1]

     new_inline_kb = await kb.inline_list2(current_list)
     await callback.message.edit_reply_markup(reply_markup = new_inline_kb)


@router.callback_query(F.data.startswith("tick_"))
# @router.callback_query()
async def tick(callback : CallbackQuery):
    logging.debug("callback data for deubug \n\n{}".format(callback))
    current_list = callback.message.reply_markup.inline_keyboard

    # Just for  DEBUG
    [logging.debug('\n {}, cb={}; b2.cb={}; b3.cb={};'.format(
        row[0].text, row[0].callback_data,
        row[1].callback_data,
        row[2].callback_data
        )) for row in current_list
    ]

    # TODO  Move to separate Class
    pressed_button_info = callback.data.split('_')
    edit_row_number = int(pressed_button_info[1])
    logging.debug('Pressed button: {} in row {}'.format(pressed_button_info[0], edit_row_number ))
    # Checking current item status: checked or unchecked
    if  current_list[edit_row_number - 1][0].callback_data == 'unchecked_{}'.format(edit_row_number):
        current_list[edit_row_number - 1][0].callback_data  = 'checked_{}'.format(edit_row_number)
        current_list[edit_row_number - 1][0].text = "✅" + current_list[edit_row_number - 1][0].text
    elif  current_list[edit_row_number - 1][0].callback_data  == 'checked_{}'.format(edit_row_number):
        current_list[edit_row_number - 1][0].callback_data  = 'unchecked_{}'.format(edit_row_number)
        current_list[edit_row_number - 1][0].text = current_list[edit_row_number - 1][0].text[1:]

    logging.debug('current_list is below:{} \n'.format(type(current_list)))
    logging.debug(current_list)
    new_inline_kb = await kb.inline_list2(current_list)
    await callback.message.edit_reply_markup(reply_markup = new_inline_kb)
    
