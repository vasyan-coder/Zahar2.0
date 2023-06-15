from __future__ import annotations

from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    chat_id: int


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'), chat_id=env.int('CHAT_ID')))
