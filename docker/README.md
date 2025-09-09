# Docker Configuration

Эта папка содержит Docker конфигурацию для проекта автоматизации тестирования OWASP JuiceShop.

## Файлы

- `docker-compose.yml` - Основной сервис для запуска тестов
- `allure-compose.yml` - Сервис Allure для отчетности
- `.env` - Переменные окружения (основные настройки)
- `.env.example` - Пример файла окружения для команды

## Быстрый старт

### 1. Настройка окружения
```bash
# Скопируй пример файла окружения
cp .env.example .env

# Настрой переменные под себя (опционально)
nano .env
```

### 2. Запуск тестов
```bash
# Из корня проекта
make test-docker

# Или напрямую
docker-compose -f docker/docker-compose.yml up --build
```

### 3. Запуск Allure сервера
```bash
# Из корня проекта
make allure-start

# Или напрямую
docker-compose -f docker/allure-compose.yml up -d
```

### 4. Просмотр отчетов
Открой в браузере: http://localhost:5050

## Переменные окружения

### Основные настройки
| Переменная | Описание | Значение по умолчанию |
|------------|----------|---------------------|
| `JUICESHOP_BASE_URL` | URL JuiceShop приложения | `http://host.docker.internal:8080` |
| `TEST_RUNNER_PORT` | Порт test runner контейнера | `4040` |
| `ALLURE_PORT` | Порт Allure сервера | `5050` |

### Ресурсы контейнера
| Переменная | Описание | Значение по умолчанию |
|------------|----------|---------------------|
| `MEMORY_LIMIT` | Лимит памяти | `1G` |
| `CPU_LIMIT` | Лимит CPU | `1` |

## Команды для разных сред

### Локальная разработка
```bash
ENVIRONMENT=local make test-docker
```

### CI/CD
```bash
ENVIRONMENT=ci JUICESHOP_BASE_URL=http://juiceshop-service:3000 make test-docker
```

### Staging
```bash
ENVIRONMENT=staging JUICESHOP_BASE_URL=https://staging.example.com make test-docker
```

## Мониторинг

### Логи тестов
```bash
docker-compose -f docker/docker-compose.yml logs -f test-runner
```

### Логи Allure
```bash
docker-compose -f docker/allure-compose.yml logs -f allure-server
```

### Статус сервисов
```bash
docker-compose -f docker/allure-compose.yml ps
```

## Устранение неполадок

### Порты заняты
Измени порты в `.env`:
```bash
TEST_RUNNER_PORT=5040
ALLURE_PORT=6050
```

### Недостаточно ресурсов
Уменьши лимиты в `.env`:
```bash
MEMORY_LIMIT=512M
CPU_LIMIT=0.5
```

### Очистка
```bash
# Остановка всех сервисов
make clean-all

# Или вручную
docker-compose -f docker/docker-compose.yml down --volumes
docker-compose -f docker/allure-compose.yml down --volumes
```