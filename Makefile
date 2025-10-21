# ========================================================
# 🚀 MakeFile for UI Support Tests with K3D
# ========================================================

# Colors for output
GREEN = \033[0;32m
RED = \033[0;31m
YELLOW = \033[1;33m
BLUE = \033[0;34m
NC = \033[0m

.PHONY: help build run test clean logs status k3d-setup allure-start allure-stop allure-report allure-restart allure-logs

# Docker compose files
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
		echo "$(RED)❌ File  $(ENV_FILE) not found!$(NC)"; \
		echo "$(YELLOW)💡 Copy example: cp $(DOCKER_DIR)/.env.example $(ENV_FILE)$(NC)"; \
		exit 1; \
	fi
endef

# ========================================================
# 🧭 HELP
# ========================================================
help: ## Show available commands and descriptions
	@echo "$(BLUE)Available commands:$(NC)"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

# ========================================================
# 🏗️ BASIC TASKS
# ========================================================
build: ## Build Docker image (use cache for speed)
	@echo "$(YELLOW)🏗️ Building Docker image $(IMAGE_NAME)...$(NC)"
	docker compose -f $(MAIN_COMPOSE) --env-file $(ENV_FILE) build

build-nocache: ## Build Docker image (ignore cache, slower but fresh)
	@echo "$(YELLOW)🏗️ Building Docker image $(IMAGE_NAME) without cache...$(NC)"
	docker compose -f $(MAIN_COMPOSE) --env-file $(ENV_FILE) build --no-cache

run: ## Run container interactively (auto remove after exit)
	@echo "$(YELLOW)🚀 Starting container $(CONTAINER_NAME)...$(NC)"
	docker compose -f $(MAIN_COMPOSE) --env-file $(ENV_FILE) run --rm $(CONTAINER_NAME)

test: ## Run tests in Docker
	$(call check_env)
	@echo "$(BLUE)🚀 Running tests inside container...$(NC)"
	@docker compose -f $(MAIN_COMPOSE) --env-file $(ENV_FILE) up --build

test-report: ## Run tests and generate Allure report
	@echo "$(BLUE)🚀 Running tests and generating Allure report...$(NC)"
	@make clean-all
	@make test
	@make allure-start

# ========================================================
# ☸️ K3D COMMANDS
# ========================================================
k3d-setup: ## Configure and create K3D cluster
	@echo "$(YELLOW)☸️ Setting up K3D cluster...$(NC)"
	@if ! k3d cluster list | grep -q $(K3D_CLUSTER); then \
		echo "$(BLUE)Creating k3d cluster $(K3D_CLUSTER)...$(NC)"; \
		k3d cluster create $(K3D_CLUSTER) \
        --servers 1 \
        --agents 1 \
        --port "8080:80@loadbalancer" \
        --port "8443:443@loadbalancer" \
        --port "2222:32222@loadbalancer" \
        --api-port 6443 \
        --k3s-arg "--disable=traefik@server:0" \
        --volume /mnt/e/Git_Projects/VirtualEnv/DockerData/k3d-shared:/data-host@all \
        --network host-network \
        --verbose \
        --wait; \
	else \
		echo "$(GREEN)Cluster $(K3D_CLUSTER) already exists$(NC)"; \
	fi
	@echo "$(GREEN)✅ Cluster ready!$(NC)"

k3d-status: ## Show K3D cluster and Kubernetes nodes
	@echo "$(YELLOW)📊 K3D cluster status:$(NC)"
	k3d cluster list
	@echo "$(YELLOW)📊 Kubernetes nodes:$(NC)"
	kubectl get nodes

k3d-clean: ## Delete K3D cluster completely
	@echo "$(YELLOW)🗑️ Removing K3D cluster $(K3D_CLUSTER)...$(NC)"
	k3d cluster delete $(K3D_CLUSTER)

# ========================================================
# ⚙️ APPLICATION MANAGEMENT
# ========================================================
app-install: ## Deploy test application (OWASP Juice Shop)
	echo  -e "${GREEN}Installing Ingress Nginx Controller${NC}"
	kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
	echo -e "${GREEN}Installing ${BLUE}OWASP Juice Shop ${GREEN}application...${NC}"
	kubectl apply -f owasp-juiceshop/juice-shop-deployment.yaml

# ========================================================
# 🧩 DEBUGGING
# ========================================================
shell: ## Enter container shell (interactive bash)
	@echo "$(YELLOW)🐚 Entering container shell...$(NC)"
	docker compose -f $(MAIN_COMPOSE) run --rm $(CONTAINER_NAME) bash || true

logs: ## Show container logs
	@echo "$(YELLOW)📜 Showing container logs...$(NC)"
	docker compose -f $(MAIN_COMPOSE) logs -f $(CONTAINER_NAME)

status: ## Show running services status
	@echo "$(YELLOW)📊 Docker services status:$(NC)"
	@docker compose -f $(MAIN_COMPOSE) ps 2>/dev/null || true

# ========================================================
# 🧹 CLEANING
# ========================================================
clean-all: ## Full cleanup (containers, images, volumes)
	@echo "$(YELLOW)🧹 Full cleanup including images...$(NC)"
	docker compose -f $(MAIN_COMPOSE) down --volumes --remove-orphans --rmi all
	docker compose -f $(ALLURE_COMPOSE) down --volumes --remove-orphans --rmi all
	docker system prune -f
	@make clean

clean: ## Remove test artifacts and cache
	@echo "$(YELLOW)🧹 Cleaning project folders...$(NC)"
	sudo rm -rf html-reports/* screenshots/* allure-results/* allure-reports/* logs/* || true
	sudo find . -type d -name "__pycache__" -prune -exec rm -rf {} + || true
	find . -name "*.pyc" -delete

# ========================================================
# 📊 ALLURE SERVER MANAGEMENT
# ========================================================
allure-start: ## Start Allure report web server
	@echo "🚀 Starting Allure server..."
	docker compose -f $(ALLURE_COMPOSE) --env-file $(ENV_FILE) up -d
	@echo "✅ Allure available: http://localhost:5050/allure/"
	@echo "✅ HTTP available: http://localhost:5050/reports/"

allure-stop: ## Stop Allure report web server
	@echo "🛑 Stopping Allure server..."
	docker compose -f $(ALLURE_COMPOSE) down

allure-restart: ## Restart Allure report web server
	@echo "🔄 Restarting Allure server..."
	docker compose -f $(ALLURE_COMPOSE) restart

allure-logs: ## Show Allure container logs
	@echo "📜 Allure logs..."
	docker compose -f $(ALLURE_COMPOSE) logs -f

allure-report: ## Generate new Allure report from results
	@echo "$(YELLOW)📈 Generating Allure report...$(NC)"
	@docker compose -f $(ALLURE_COMPOSE) exec -T allure-server sh -c "allure generate --clean allure-results -o allure-report"
