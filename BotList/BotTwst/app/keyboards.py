from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from aiogram.utils import keyboard
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import logging

main = ReplyKeyboardMarkup(keyboard=[
	[KeyboardButton(text="New list")],
	[KeyboardButton(text="Edit list")]
	],
						   resize_keyboard=True,
						   input_field_placeholder="Chose an option")

async def inline_list(products, ticked=False):
	keyboard = InlineKeyboardBuilder()
	raw = 0
	for product in products:
		raw = raw + 1
		if ticked:
			tic_text = "✅"
		else:
			tic_text = "❌"

		keyboard.add(InlineKeyboardButton(text=product, callback_data=f"unchecked_{raw}"))
		keyboard.add(InlineKeyboardButton(text=tic_text, callback_data=f"tick_{raw}"))
		keyboard.add(InlineKeyboardButton(text="🗑", callback_data=f"del_{raw}"))
	
	logging.debug("whole keyboard {}".format(keyboard.adjust(3).as_markup()))
	return keyboard.adjust(3).as_markup()
	
async def inline_list2(_keybord):
	new_keyboard = InlineKeyboardBuilder()
	#raw = 0
	for rows in _keybord:
		for button in rows:
		    new_keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.callback_data))
	
	#logging.debug("whole keyboard2: {}".format(new_keyboard.adjust(3).as_markup()))
	return new_keyboard.adjust(3).as_markup()
