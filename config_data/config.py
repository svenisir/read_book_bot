from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str            # Токен для доступа к телеграм-боту


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str=None) -> Config:
    # Создаем экземпляр класса Env
    # Добавляем в переменные окружения данные, прочитанные из файла .env
    env: Env = Env()
    env.read_env(path)

    # Создаем экземпляр класса Config и наполняем его данными из переменных окружения
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')))
