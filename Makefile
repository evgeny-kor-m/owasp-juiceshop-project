# MakeFile for UI Support Tests K3D

# Colors for output
GREEN = \033[0;32m
RED = \033[0;31m
YELLOW = \033[1;33m
BLUE = \033[0;34m
NC = \033[0m

.PHONY: help build run test clean logs status k3d-setup k3d-import web-reports

# Docker compose файлы
DOCKER_DIR = docker
MAIN_COMPOSE = $(DOCKER_DIR)/docker-compose.yml
ALLURE_COMPOSE = $(DOCKER_DIR)/allure-compose.yml
ENV_FILE = $(DOCKER_DIR)/.env

# Variables
K3D_CLUSTER = test-lab
IMAGE_NAME = test-runner:latest
CONTAINER_NAME = test-runner

# Checking if exists .env file
define check_env
	@if [ ! -f $(ENV_FILE) ]; then \
		echo "$(RED)❌ Файл $(ENV_FILE) не найден!$(NC)"; \
		echo "$(YELLOW)💡 Скопируй пример: cp $(DOCKER_DIR)/.env.example $(ENV_FILE)$(NC)"; \
		exit 1; \
	fi
endef


help: ## show the certificate. Disputes a list of all available commands with their descriptions
	@echo "$(YELLOW)🚀 UI Testing с поддержкой k3d$(NC)"
	@echo "$(BLUE)Доступные команды:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# === Basic teams ===
build: ## Collect Docker image. For everyday development, to use the Docker cache by default, which will significantly speed up repeated assemblies.
	@echo "$(YELLOW)🏗️ Сборка Docker образа $(IMAGE_NAME)...$(NC)"
	docker-compose -f $(MAIN_COMPOSE) --env-file $(ENV_FILE) build

build-nocache: ## Collect Docker image. [-NO-CACHE] makes doCker rebuild all layers, ignoring the cache, which is useful to ensure fresh assembly, but can be slower.
	@echo "$(YELLOW)🏗️ Сборка Docker образа $(IMAGE_NAME)...$(NC)"
	docker-compose -f $(MAIN_COMPOSE) --env-file $(ENV_FILE) build --no-cache

run: ## Run the container interactive. Wedding mode (-rm deleys the container after completion).
	@echo "$(YELLOW)🚀 Запуск контейнера $(CONTAINER_NAME)...$(NC)"
	docker-compose -f $(MAIN_COMPOSE) run --rm $(CONTAINER_NAME)


# === debugging ===
shell: ## enter the container
	@echo "$(YELLOW)🐚 Вход в контейнер...$(NC)"
	docker-compose -f $(MAIN_COMPOSE) run --rm $(CONTAINER_NAME) bash || true

logs: ## Show Log
	@echo "$(YELLOW)📜 Логи контейнера:$(NC)"
	docker-compose -f $(MAIN_COMPOSE) logs -f $(CONTAINER_NAME)

status: ## show the status of services.
	@echo "$(YELLOW)📊 Статус сервисов:$(NC)"
	docker-compose -f $(MAIN_COMPOSE) ps

# === management ===
clean: ## Clean the reports and stop the services. He stops and deleys all services and their anonymous volumes, as well as “orphaned” containers.
	@echo "$(YELLOW)🧹 Очистка...$(NC)"
	docker-compose -f $(MAIN_COMPOSE) down --volumes --remove-orphans
	docker-compose -f $(ALLURE_COMPOSE) down --volumes --remove-orphans
	sudo rm -rf reports/* screenshots/* allure-results/* allure-report/* logs/*

clean-all: clean ## complete cleaning (including images). Recommendation: Use carefully
## Docker-Compose ... Down --romi all (deleys the images used by services) and Docker System Prune -f (removes unused Docker objects).
	@echo "$(YELLOW)🧹 Полная очистка (включая образы)...$(NC)"
	docker-compose -f $(MAIN_COMPOSE) down --volumes --remove-orphans --rmi all
	docker-compose -f $(ALLURE_COMPOSE) down --volumes --remove-orphans --rmi all
	docker system prune -f

clear-cache: ## Очистка кэша
	@echo "$(YELLOW)🧹 Очистка кэша...$(NC)"
	find . -type d -name "__pycache__" -delete
	find . -name "*.pyc" -delete

# === Allure server management ===
allure-start:
	@echo "🚀 Запуск Allure сервера..."
	docker-compose -f $(ALLURE_COMPOSE) up -d
	@echo "✅ Allure доступен: http://localhost:5050"

allure-stop:
	@echo "🛑 Остановка Allure сервера..."
	docker-compose -f $(ALLURE_COMPOSE) down

allure-restart:
	@echo "🔄 Перезапуск Allure сервера..."
	docker-compose -f $(ALLURE_COMPOSE) restart

# Логи Allure сервера
allure-logs:
	docker-compose -f $(ALLURE_COMPOSE) logs -f