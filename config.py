import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


class Config:
    VK_GROUP_ID: int = int(os.getenv('VK_GROUP_ID', 0))
    VK_ACCESS_TOKEN: str = os.getenv('VK_ACCESS_TOKEN', '')
    BASE_DIR: Path = Path(__file__).parent
    DATABASE_PATH: Path = BASE_DIR / 'data' / 'bot_database.db'

    AUTHOR_GROUP: str = "545-M"

    AUTHORS: list = [
        {"name": "Бантя Александр", "vk": "https://vk.com/san400ys"},
        {"name": "Нильмаер Иван", "vk": "https://vk.com/vanish_bb"},
        {"name": "Сумин Артем", "vk": "https://vk.com/local_satan"},
    ]

    AUTHOR_INFO: str = "👨‍💻 АВТОРЫ ПРОЕКТА\n\nГруппа: " + AUTHOR_GROUP + "\n\n" + "\n".join(
        [f"{a['name']}\n   ВК: {a['vk']}\n" for a in AUTHORS]
    )

    BLOG_POSTS: list = [
        "📰 Новость 1: Крутая новость 1",
        "📰 Новость 2: Крутая новость 2",
        "📰 Новость 3: Крутая новость 3"
    ]

    STATE_FEE_BRACKETS: list = [
        (100_000, 4_000, 0),
        (300_000, 4_000, 0.03),
        (500_000, 10_000, 0.025),
        (1_000_000, 15_000, 0.02),
        (3_000_000, 25_000, 0.01),
        (8_000_000, 45_000, 0.007),
        (24_000_000, 80_000, 0.0035),
        (50_000_000, 136_000, 0.003),
        (100_000_000, 214_000, 0.002),
        (float('inf'), 314_000, 0.0015)
    ]
    MAX_STATE_FEE: int = 900_000

    PENALTY_RATE_1_90: float = 1 / 300
    PENALTY_RATE_91_180: float = 1 / 170
    PENALTY_RATE_181_PLUS: float = 1 / 130
    REFINANCING_RATE: float = 0.21


config = Config()