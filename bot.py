from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor
from aiogram.types import InputFile
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code
from aiogram.types import ParseMode
from random import seed, randrange
from time import time

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

faculty = ["матфак", "экономфак", "миэм", "компьютерные науки", "высшая школа бизнеса", "право",
           "юриспруденция и администрирование", "гуманитарные науки", "социальные науки", "креативные индустрии",
           "мировая экономика и мировая политики", "физика", "миэф", "городское и региональное развитие", "химфак",
           "биофак", "геофак", "иняз", "лицей вышки", "хогвартс"]
cats = ["images/cat1.jpg", "images/cat2.jpg", "images/cat3.jpg", "images/cat4.jpg", "images/cat5.jpg"]
quotes = [
    'Если ты плачешь не от счастья, то перестань.',
    'Чтобы выигрывать, прежде всего нужно играть.',
    'Жить надо так, чтобы тебя помнили и сволочи.',
    'Нельзя выиграть, если ты только защищаешься. Чтобы выиграть, нужно идти в атаку.',
    'К черту совершенство. Не надо его добиваться. Надо развиваться. Пусть фишки ложатся как ложатся.'
]
authors = ['Futurama', 'Альберт Эйнштейн', 'Фаина Раневская', 'Death Note', 'Чак Паланик, "Бойцовский клуб"']
kb = [
    [types.KeyboardButton(text="Кринж")],
    [types.KeyboardButton(text="Цитатка")],
    [types.KeyboardButton(text="Котик")],
    [types.KeyboardButton(text="Распределение")]
]
keyboard = types.ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True,
    input_field_placeholder="Или отправь мне что-нибудь"
)


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    kb_start = [
        [types.KeyboardButton(text="Да!")],
        [types.KeyboardButton(text="Нет:(")]
    ]
    keyboard_start = types.ReplyKeyboardMarkup(
        keyboard=kb_start,
        resize_keyboard=True,
        input_field_placeholder="Не обманывай себя"
    )
    await message.answer("Привет. Ты учишься в Вышке и ещё жив(а)?", reply_markup=keyboard_start)


@dp.message_handler(lambda message: message.text and 'да' in message.text.lower())
async def alive(message: types.Message):
    await message.reply("Молодец, держи пирожок", reply_markup=types.ReplyKeyboardRemove())
    photo = InputFile(f"images/pie.jpg")
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await message.answer("Смотри, что я умею. Выбери, чего ты хочешь:", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text and 'нет' in message.text.lower())
async def not_alive(message: types.Message):
    await message.reply("Не грусти, все мы там будем", reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Смотри, что я умею. Выбери, чего ты хочешь:", reply_markup=keyboard)


@dp.message_handler(commands=['help'])
async def help_message(message):
    await message.answer("Смотри, что я умею. Выбери, чего ты хочешь:", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text and 'кринж' in message.text.lower())
async def cringe(message: types.Message):
    try:
        seed(int(time()))
        number = randrange(0, 100)
        message_text = text("Ты кринж на", number, "процентов, а я на 100!")
        await message.reply(message_text)
    except Exception as e:
        print("{!s}\n{!s}".format(type(e), str(e)))


@dp.message_handler(lambda message: message.text and 'цитатка' in message.text.lower())
async def quote_ceremony(message: types.Message):
    try:
        seed(int(time()))
        quote_number = randrange(0, 4)
        message_text = text(quotes[quote_number], '\n', bold(authors[quote_number]))
        photo = InputFile(f"images/wolf.jpg")
        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=message_text, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        print("{!s}\n{!s}".format(type(e), str(e)))


@dp.message_handler(lambda message: message.text and 'котик' in message.text.lower())
async def cats_ceremony(message: types.Message):
    try:
        seed(int(time()))
        cat_number = randrange(0, 4)
        photo = InputFile(cats[cat_number])
        caption = 'Твой котик дня:3'
        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=caption)
    except Exception as e:
        print("{!s}\n{!s}".format(type(e), str(e)))


@dp.message_handler(lambda message: message.text and 'распределение' in message.text.lower())
async def sorting_ceremony(message: types.Message):
    try:
        seed(int(time()))
        faculty_number = randrange(0, 20)
        message_text = text("Твой факультет: ", bold(faculty[faculty_number]), ", поздравляю!")
        await message.reply(message_text, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        print("{!s}\n{!s}".format(type(e), str(e)))


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(message: types.Message):
    message_text = text(italic('Я не знаю, что с этим делать'), ':(',
                        '\nНо у меня есть',
                        code('команда'), '/help')
    await message.reply(message_text, parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    executor.start_polling(dp)
