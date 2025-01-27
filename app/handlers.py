from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb

import logging

router = Router()

class DialogStatus(StatesGroup):
    wait_items = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Hello, I'm a shopping list bot.\nIf you need create a new list or edit existing, use button bellow \nFor other information use /help",
                      reply_markup=kb.main)

@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer("The bot allows you to create shopping/task lists \nCommand list: \n/help - calls this message, with information about all commands and basic instructions for use \n/start - command to start interacting with the bot \nSend 'New list' or use button next to the message box - allows you to create a new list, to do this, you need to write the elements of the list separating them with a paragraph \n\nInstructions. \nTo create a new list, write 'New list' or use button next to the message box, then write your products/tasks separating them with a paragraph, then send a message \nThe bot will send you a list. If the name does not fit in the first section, you can click on it to see its full name. The second button (✅) is responsible for marking your product, when you click on it, it will mark your product as checked. The third button (🗑) allows you to delete a separate section from the list. \nAt a time, you can have an unlimited number of lists. If you want to use the previous list as a basis, copy your message with the previous list. To delete an entire list, select the message with the list and delete it by standard Telegram function. \nThe bot automatically sorts your sections alphabetically and by marked/unmarked order. \nTo use the bot with multiple people, add it to a group chat and make him an admin of the group chat ", reply_markup=kb.main)

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
        
#######################################################
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

#######################################################

class ListItems:
    def __init__(self, _items) -> None:
        self.list_of_rows = _items
    
    def _renumerate(self):
        for i, row in enumerate(self.list_of_rows, start=1):
            if row[0].callback_data.startswith("unchecked_"):
                row[0].callback_data = f'unchecked_{i}'
            elif row[0].callback_data.startswith("checked_"):
                row[0].callback_data = f'checked_{i}'
            row[1].callback_data = f'tick_{i}'
            row[2].callback_data = f'del_{i}'

    def switch_checked(self, _row_number):
        """
        Set checked ✅  in string if not set yet
        """
        def _buid_sortkey(array_member):
            """
            Just build and returns the key for sorting
            """
            return array_member[0].text

        # Checking current item status: checked or unchecked
        if   self.list_of_rows[_row_number - 1][0].callback_data == 'unchecked_{}'.format(_row_number):
             self.list_of_rows[_row_number - 1][0].callback_data  = 'checked_{}'.format(_row_number)
             self.list_of_rows[_row_number - 1][0].text = "✅" +  self.list_of_rows[_row_number - 1][0].text
        elif   self.list_of_rows[_row_number - 1][0].callback_data  == 'checked_{}'.format(_row_number):
             self.list_of_rows[_row_number - 1][0].callback_data  = 'unchecked_{}'.format(_row_number)
             self.list_of_rows[_row_number - 1][0].text =  self.list_of_rows[_row_number - 1][0].text[1:]
        
        self.list_of_rows.sort(key=_buid_sortkey)
        self._renumerate()
    
    def remove_item(self, _row_number):
        def _buid_sortkey(array_member):
            """
            Just build and returns the key for sorting
            """
            return array_member[0].text

        """
        Remove item from list (remove one string with buttons)
        """
        del self.list_of_rows[_row_number-1]
        self._renumerate()
        self.list_of_rows.sort(key=_buid_sortkey)