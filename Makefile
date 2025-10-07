# Makefile for UI Support Tests K3D

# Colors for output
GREEN = \033[0;32m
RED = \033[0;31m
YELLOW = \033[1;33m
BLUE = \033[0;34m
NC = \033[0m

.PHONY: help build run test clean logs status k3d-setup k3d-import web-reports

# Docker compose files
DOCKER_DIR = docker
MAIN_COMPOSE = $(DOCKER_DIR)/docker-compose.yml
ALLURE_COMPOSE = $(DOCKER_DIR)/allure-compose.yml
ENV_FILE = $(DOCKER_DIR)/.env

# Variables
K3D_CLUSTER = test-lab
IMAGE_NAME = test-runner:latest
CONTAINER_NAME = test-runner

# Checking if .env file exists
define check_env
	@if [ ! -f $(ENV_FILE) ]; then \
		echo "$(RED)❌ File $(ENV_FILE) not found!$(NC)"; \
		echo "$(YELLOW)💡 Copy example: cp $(DOCKER_DIR)/.env.example $(ENV_FILE)$(NC)"; \
		exit 1; \
	fi
endef


help: ## show this help. Displays a list of all available commands with their descriptions
	@echo "$(YELLOW)🚀 UI Testing with k3d support$(NC)"
	@echo "$(BLUE)Available commands...$(NC)" # (Rest of help output truncated)

logs: ## show logs of all running services.
	@echo "$(YELLOW)📄 Service logs:$(NC)"
	@docker compose -f $(MAIN_COMPOSE) logs -f 2>/dev/null || true
	@docker compose -f $(ALLURE_COMPOSE) logs -f 2>/dev/null || true

build: ## build the test runner image.
	@$(call check_env)
	@echo "$(YELLOW)🛠️ Building Docker image: $(IMAGE_NAME)$(NC)"
	docker build -f $(DOCKER_DIR)/Dockerfile -t $(IMAGE_NAME) .
	@echo "$(GREEN)✅ Image built successfully.$(NC)"

run: ## run all services (docker-compose up).
	@$(call check_env)
	@echo "$(YELLOW)🚀 Starting all services...$(NC)"
	@docker compose -f $(MAIN_COMPOSE) --env-file $(ENV_FILE) up -d --build
	@make status
	@echo "$(GREEN)✅ Services started. Test runner is available: http://localhost:$(TEST_RUNNER_PORT)$(NC)"

stop: ## stop all running services.
	@echo "$(YELLOW)🛑 Stopping all services...$(NC)"
	@docker compose -f $(MAIN_COMPOSE) down --volumes --remove-orphans
	@make allure-stop
	@echo "$(GREEN)✅ All services stopped.$(NC)"

test: ## run tests inside the container.
	@$(call check_env)
	@echo "$(YELLOW)🧪 Running tests inside container $(CONTAINER_NAME)...$(NC)"
	@docker compose -f $(MAIN_COMPOSE) exec -T $(CONTAINER_NAME) bash -c "pytest --alluredir=allure-results/ --html=reports/report.html --self-contained-html -v"
	@echo "$(GREEN)✅ Tests finished. Results in allure-results/ and reports/report.html.$(NC)"

web-reports: ## build and open the HTML test report.
	@echo "$(YELLOW)📄 Building and opening HTML report...$(NC)"
	@if [ -f reports/report.html ]; then open reports/report.html; else echo "$(RED)❌ Report file reports/report.html not found.$(NC)"; fi

status: ## show the status of services.
	@echo "$(YELLOW)📊 Service status:$(NC)"
	@docker compose -f $(MAIN_COMPOSE) ps 2>/dev/null || true
	@docker compose -f $(ALLURE_COMPOSE) ps 2>/dev/null || true

# === management ===

clean-all: ## complete cleaning (including images). Recommendation: Use carefully
## docker compose ... Down --romi all (removes the images used by services) and Docker System Prune -f (removes unused Docker objects).
	@echo "$(YELLOW)🧹 Full cleanup (including images)...$(NC)"
	docker compose -f $(MAIN_COMPOSE) down --volumes --remove-orphans --rmi all
	docker compose -f $(ALLURE_COMPOSE) down --volumes --remove-orphans --rmi all
	docker system prune -f
	@make clean

clean: ## cleanup temporary files, logs, and reports.
	@echo "$(YELLOW)🧹 Cleanup...$(NC)"
	sudo rm -rf reports/* screenshots/* allure-results/* allure-report/* logs/* || true
	sudo find . -type d -name "__pycache__" -prune -exec rm -rf {} +\
	find . -name "*.pyc" -delete

# === Allure server management ===
allure-start: ## start Allure report server.
	@echo "🚀 Starting Allure server..."
	docker compose -f $(ALLURE_COMPOSE) --env-file $(ENV_FILE) up -d
	@echo "✅ Allure is available: http://localhost:505..."

allure-stop: ## stop Allure server.
	@echo "🛑 Stopping Allure server..."
	docker compose -f $(ALLURE_COMPOSE) down
	@echo "✅ Allure server stopped."

allure-report: ## generate an Allure report from results and open it.
	@echo "$(YELLOW)📈 Generating and opening Allure report...$(NC)"
	@docker compose -f $(ALLURE_COMPOSE) exec -T allure sh -c "allure generate --clean allure-results -o allure-report"
	@open allure-report/index.html

# === k3d management (if used) ===

k3d-setup: ## set up k3d cluster and registries.
	@echo "$(YELLOW)⚙️ Setting up k3d cluster: $(K3D_CLUSTER)$(NC)"
	# Check if cluster exists
	k3d cluster create $(K3D_CLUSTER) --registry-create registry.localhost:5000 || (echo "$(RED)❌ Cluster creation error!$(NC)"; exit 1)
	@echo "$(GREEN)✅ k3d cluster $(K3D_CLUSTER) created.$(NC)"

k3d-import: ## load the Docker image into the k3d cluster.
	@echo "$(YELLOW)📦 Loading image $(IMAGE_NAME) into k3d cluster...$(NC)"
	k3d image import $(IMAGE_NAME) -c $(K3D_CLUSTER) || (echo "$(RED)❌ Image loading error!$(NC)"; exit 1)
	@echo "$(GREEN)✅ Image $(IMAGE_NAME) loaded into cluster $(K3D_CLUSTER).$(NC)"

k3d-delete: ## delete the k3d cluster.
	@echo "$(YELLOW)💥 Deleting k3d cluster: $(K3D_CLUSTER)...$(NC)"
	k3d cluster delete $(K3D_CLUSTER) || true
	@echo "$(GREEN)✅ Cluster $(K3D_CLUSTER) deleted.$(NC)"