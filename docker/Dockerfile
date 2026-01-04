# Dockerfile
# Используем официальный образ Python как базовый
FROM python:3.12-slim-bookworm

# wget for downloading files, curl for general networking, and openjdk for allure
RUN apt-get update && apt-get install -y --no-install-recommends \
    make \
    wget \
    curl \
    gnupg \
    unzip \
    openjdk-17-jdk \
    # Clean the APT-GET cache to reduce the size of the image
    && rm -rf /var/lib/apt/lists/*

# Download the current version of Allure Framework
# Allure Cli is necessary to generate beautiful interactive reports on the test results.
# WGET: downloads the Allure archive.
# TAR -xF: unpacked the archive.
# MV: moves the unpacked folder in /opt /allure.
# ln -s: creates a symbolic link so that the 'Allure' command can be called from any place.
# rm allure.tgz: removes the loaded archive to reduce the size of the image.
RUN wget -O allure.tgz https://github.com/allure-framework/allure2/releases/download/2.34.1/allure-2.34.1.tgz \
    && tar -xf allure.tgz \
    && mv allure-2.34.1 /opt/allure \
    && ln -s /opt/allure/bin/allure /usr/local/bin/allure \
    && rm allure.tgz

# =========================
# Google Chrome (for Selenium)
# =========================
RUN curl -fsSL https://dl-ssl.google.com/linux/linux_signing_key.pub \
        | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/google-chrome.gpg] \
        http://dl.google.com/linux/chrome/deb/ stable main" \
        > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# =========================
# Python environment
# =========================
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта в контейнер
COPY . /app

# Команда по умолчанию, которая будет выполнена при запуске контейнера
# Используем `python -m pytest` для корректного обнаружения модулей
CMD ["python", "-m", "pytest", "test_automation_framework/tests"]