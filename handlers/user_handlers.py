import requests as requests
from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from bs4 import BeautifulSoup

from lexicon.lexicon_ru import LEXICON_RU

# Инициализируем роутер уровня модуля
router: Router = Router()

zodiac_translate: dict[str, str] = {
    "овен": "aries",
    "телец": "taurus",
    "близнецы": "gemini",
    "рак": "cancer",
    "лев": "leo",
    "дева": "virgo",
    "весы": "libra",
    "скорпион": "scorpio",
    "стрелец": "sagittarius",
    "козерог": "capricorn",
    "водолей": "aquarius",
    "рыбы": "pisces",
}


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


# Функция, которая будет запускаться по расписанию
async def send_daily_image(bot: Bot, chat_id: int):
    await bot.send_message(chat_id, "Hello")


@router.message(Command(commands='гороскоп'))
async def process_horo_command(message: Message):
    zodiac_forecast: str = await __parse_horo(message.text.split()[1])
    await message.answer(text=zodiac_forecast)


async def __parse_horo(zodiac: str) -> str:
    if await __check_zodiac(zodiac):
        url = f'https://horo.mail.ru/prediction/{zodiac_translate.get(zodiac)}/today/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        text_horo = soup.find("div", class_="article__item article__item_alignment_left article__item_html").text
        return text_horo
    else:
        return "Звезды говорят, что ты пидр и такого знака не существует"


async def __check_zodiac(zodiac: str) -> bool:
    return zodiac in zodiac_translate
