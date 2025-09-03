# Используем официальный образ Python как базовый
FROM python:3.12-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта в контейнер
COPY . .

# Команда по умолчанию, которая будет выполнена при запуске контейнера
# Используем `python -m pytest` для корректного обнаружения модулей
CMD ["python", "-m", "pytest", "test_automation_framework/tests"]