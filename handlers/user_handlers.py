import random

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
    start: int = 1000
    end: int = 1898

    with open('used_img.txt', 'r') as f:
        used_numbers = f.read().splitlines()

    used_numbers = [int(num) for num in used_numbers]

    if len(used_numbers) <= end - start + 1:
        # Генерируем число, которое еще не было использовано
        while True:
            new_number = random.randint(start, end)
            if new_number not in used_numbers:
                break
    else:
        with open('used_img.txt', 'w') as f:
            f.write('')
        used_numbers = []
        new_number = random.randint(start, end)

    used_numbers.append(new_number)
    with open('used_img.txt', 'w') as f:
        for number in used_numbers:
            f.write(str(number) + '\n')
    await bot.send_photo(chat_id=chat_id,
                         photo=f"https://raw.githubusercontent.com/0niel/happy-new-day/main/images/{new_number}.jpg")


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
