import os
from pathlib import Path
from dotenv import load_dotenv

# Находим корень проекта автоматически
# (поднимаемся на 2 уровня выше от /config/config.py)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Загружаем .env из корня
load_dotenv(BASE_DIR / ".env")

class Settings:
    # Используем os.getenv(ключ, дефолтное_значение)
    APP_URL: str = os.getenv("APP_URL", "[https://default.url](https://default.url)")
    API_KEY: str = os.getenv("API_KEY", "")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()