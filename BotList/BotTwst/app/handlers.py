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

class DialogStatus(StatesGroup):
    wait_items = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Hello, I'm a shopping list bot.\n If you need create a new list or edit existing, use button bellow \n For other information use /help",
                      reply_markup=kb.main)

@router.message(F.text == "New list")
async def process_new_list(message: Message, state: FSMContext):
    await state.set_state(DialogStatus.wait_items)
    await message.answer("Write your products separating by paragraphs")

@router.message(DialogStatus.wait_items)
async def process_list_items(message: Message, state: FSMContext):
    await state.update_data(list=message.text)
    data = await state.get_data()   
    products = data["list"].splitlines()
    inline_kb = await kb.inline_list(products)
    await message.answer("Your list", reply_markup=inline_kb)
    await state.clear()

######################################################3
#######################################################

@router.callback_query(F.data.startswith("tick_"))
async def cb_process_check(callback : CallbackQuery):
    logging.debug("callback data for deubug - check \n\n{}".format(callback))
    current_list = callback.message.reply_markup.inline_keyboard

    # Just for  DEBUG
    [logging.debug('\n {}, cb={}; b2.cb={}; b3.cb={};'.format(
        row[0].text, row[0].callback_data,
        row[1].callback_data,
        row[2].callback_data
        )) for row in current_list
    ]
    
    pressed_button_info = callback.data.split('_')
    edit_row_number = int(pressed_button_info[1])
    logging.debug('Pressed button: {} in row {}'.format(pressed_button_info[0], edit_row_number ))

    items_list = ListItems(callback.message.reply_markup.inline_keyboard)
    items_list.switch_checked(edit_row_number)
    
    logging.debug('current_list is below:{} \n'.format(type(items_list.list_of_rows)))
    logging.debug(items_list.list_of_rows)

    new_inline_kb = await kb.inline_list2(items_list.list_of_rows)
    await callback.message.edit_reply_markup(reply_markup = new_inline_kb)

@router.callback_query(F.data.startswith("del_"))
async def cb_process_delete(callback : CallbackQuery):
    logging.debug("callback data for deubug - delete \n\n{}".format(callback))

    pressed_button_info = callback.data.split('_')
    edit_row_number = int(pressed_button_info[1])
    logging.debug('Pressed button: {} in row {}'.format(pressed_button_info[0], edit_row_number ))

    items_list = ListItems(callback.message.reply_markup.inline_keyboard)
    items_list.remove_item(edit_row_number)

    new_inline_kb = await kb.inline_list2(items_list.list_of_rows)
    await callback.message.edit_reply_markup(reply_markup = new_inline_kb)

@router.callback_query(F.data.startswith("unchecked_"))
# Tried to do it with ("unchecked_" or "checked_"), but couldn't, so did it with 2 different def
async def name(callback : CallbackQuery):
    current_list = callback.message.reply_markup.inline_keyboard
    pressed_button_info = callback.data.split('_')
    edit_row_number = int(pressed_button_info[1])
    await callback.answer(current_list[edit_row_number - 1][0].text)
    
@router.callback_query(F.data.startswith("checked_"))
# Tried to do it with ("unchecked_" or "checked_"), but couldn't, so did it with 2 different def
async def name(callback : CallbackQuery):
    current_list = callback.message.reply_markup.inline_keyboard
    pressed_button_info = callback.data.split('_')
    edit_row_number = int(pressed_button_info[1])
    await callback.answer(current_list[edit_row_number - 1][0].text)

#############################################################

class ListItems:
    def __init__(self, _items) -> None:
        self.list_of_rows = _items
    
    def switch_checked(self, _row_number):
        """
        Set checked ✅  in string if not set yet
        """
        # Checking current item status: checked or unchecked
        if   self.list_of_rows[_row_number - 1][0].callback_data == 'unchecked_{}'.format(_row_number):
             self.list_of_rows[_row_number - 1][0].callback_data  = 'checked_{}'.format(_row_number)
             self.list_of_rows[_row_number - 1][0].text = "✅" +  self.list_of_rows[_row_number - 1][0].text
        elif   self.list_of_rows[_row_number - 1][0].callback_data  == 'checked_{}'.format(_row_number):
             self.list_of_rows[_row_number - 1][0].callback_data  = 'unchecked_{}'.format(_row_number)
             self.list_of_rows[_row_number - 1][0].text =  self.list_of_rows[_row_number - 1][0].text[1:]
    
    def remove_item(self, _row_number):
        """
        Remove item from list (remove one string with buttons)
        """
        del self.list_of_rows[_row_number]
    