# MakeFile for UI Support Tests K3D

# Variables
COMPOSE_FILE = docker-compose.yml
K3D_CLUSTER = test-lab
IMAGE_NAME = test-runner:latest
CONTAINER_NAME = test-runner
#MOUNT_PATH = /home/appuser/projects/testing-lab-project-root/env-settings/docker/common-container/

# Colors for output
GREEN = \033[0;32m
RED = \033[0;31m
YELLOW = \033[1;33m
BLUE = \033[0;34m
NC = \033[0m

.PHONY: help build run test clean logs status k3d-setup k3d-import web-reports

help: ## show the certificate. Disputes a list of all available commands with their descriptions.
	@echo "$(YELLOW)🚀 UI Testing с поддержкой k3d$(NC)"
	@echo "$(BLUE)Доступные команды:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

run: ## Run the container interactive. Wedding mode (-rm deleys the container after completion).
    @echo "$(YELLOW)🚀 Запуск контейнера $(CONTAINER_NAME)...$(NC)"
    docker-compose -f $(COMPOSE_FILE) run --rm $(CONTAINER_NAME)