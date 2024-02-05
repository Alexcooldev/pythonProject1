import asyncio

from aiogram.filters import CommandStart, Command, or_f
from aiogram.utils.formatting import as_list, as_marked_section, Bold
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import (BotCommandScopeAllPrivateChats, BotCommand, ReplyKeyboardMarkup, KeyboardButton,
                           ReplyKeyboardRemove)

TOKEN = '6765117166:AAGrY69ewEGo_e9P-dwfW_CylyTyxuv_oKQ'
ALLOWED_UPDATES = ['message, edited_message']
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
private = [
    BotCommand(command='menu', description='Посмотреть меню'),
    BotCommand(command='about', description='О нас'),
    BotCommand(command='payment', description='Варианты оплаты'),
    BotCommand(command='shipping', description='Варианты доставки'),
]
start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Меню'),
            KeyboardButton(text='О магазине'),
        ],
        {
            KeyboardButton(text='Варианты доставки'),
            KeyboardButton(text='Варианты оплаты'),
        },
        {
            KeyboardButton(text='Отправить номер', request_contact=True),
            #KeyboardButton(text='Отправить локацию', request_location=True),
        }
    ],
    resize_keyboard=True,
    input_field_placeholder='Что Вас интересует?'
)
del_kb = ReplyKeyboardRemove()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Привет, я виртуальный помощник', reply_markup=start_kb)

@dp.message(or_f(Command('menu'), (F.text.lower() == 'меню')))
async def menu_cmd(message: types.Message):
    await message.answer('Вот меню:')

@dp.message(F.text.lower() == 'о нас')
@dp.message(Command('about'))
async def about_cmd(message: types.Message):
    await message.answer('О нас:')


@dp.message(F.text.lower() == 'варианты оплаты')
@dp.message(Command('payment'))
async def payment_cmd(message: types.Message):
    text = as_marked_section(
           Bold('Варианты оплаты:'),
    'Картой в боте',
           'При получении карта/кэш',
           marker='!!!'
    )
    await message.answer(text.as_html())

@dp.message(F.text.lower() == 'варианты доставки')
@dp.message(Command('shipping'))
async def shipping_cmd(message: types.Message):
    text = as_list(
        as_marked_section(
            Bold('Варианты доставки/заказа:'),
            'Курьер',
            'Самовынос (сейчас прибегу заберу)',
            'Покушаю на месте (уже бегу)',
            marker='!!!'
        ),
        as_marked_section(
            Bold('Нельзя:'),
            'Белпочтой',
            'Голубиной почтой',
            marker='**'
        ),
        sep='\n---------------------------\n'
    )
    await message.answer(text.as_html())

@dp.message(F.contact)
async def get_contact(message: types.Message):
    await message.answer(f'номер получен')
    await message.answer(str(message.contact.phone_number))

#@dp.message(F.location)
#async def get_location(message: types.Message):
# await message.answer(f'локация получена')
#await message.answer(str(message.location))

async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())
