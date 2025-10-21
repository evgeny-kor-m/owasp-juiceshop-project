# MakeFile for UI Support Tests K3D.

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

# Checking if exists .env file
define check_env
	@if [ ! -f $(ENV_FILE) ]; then \
		echo "$(RED)❌ File  $(ENV_FILE) not found!$(NC)"; \
		echo "$(YELLOW)💡 Copy example: cp $(DOCKER_DIR)/.env.example $(ENV_FILE)$(NC)"; \
		exit 1; \
	fi
endef


help: ## show the certificate. Disputes a list of all available commands with their descriptions
	@echo "$(YELLOW)🚀 UI Testing with k3d support $(NC)"
	@echo "$(BLUE)Available commands:$(NC)"
#	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@grep make -pr | awk -F: '/^[a-zA-Z0-9_-]+:([^=]|$)/ {print $1}' | sort

# === Basic teams ===
build: ## Collect Docker image. For everyday development, to use the Docker cache by default, which will significantly speed up repeated assemblies.
	@echo "$(YELLOW)🏗️ Building Docker image $(IMAGE_NAME)...$(NC)"
	docker compose -f $(MAIN_COMPOSE) --env-file $(ENV_FILE) build

build-nocache: ## Collect Docker image. [-NO-CACHE] makes doCker rebuild all layers, ignoring the cache, which is useful to ensure fresh assembly, but can be slower.
	@echo "$(YELLOW)🏗️ Building Docker image $(IMAGE_NAME)...$(NC)"
	docker compose -f $(MAIN_COMPOSE) --env-file $(ENV_FILE) build --no-cache

run: ## Run the container interactive. Wedding mode (-rm delete the container after completion).
	@echo "$(YELLOW)🚀 Starting container $(CONTAINER_NAME)...$(NC)"
	docker compose -f $(MAIN_COMPOSE) --env-file $(ENV_FILE) run --rm $(CONTAINER_NAME)

test: ## Run tests in Docker
	$(call check_env)
	@echo "$(BLUE)🚀 Running tests inside container...$(NC)"
	@docker compose -f $(MAIN_COMPOSE) --env-file $(ENV_FILE) up --build

test-report: ## Run tests and reports
	@echo "$(BLUE)🚀 Running tests, Starting Allure...$(NC)"
	@make clean-all
	@make test
	@make allure-start

# === K3D commands ===
k3d-setup: ## configure k3d cluster
	@echo "$(YELLOW)☸️ Settings k3d cluster...$(NC)"
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
		echo "$(GREEN)Cluster $(K3D_CLUSTER) already created$(NC)"; \
	fi
	@echo "$(GREEN)✅ Cluster ready!$(NC)"

k3d-status: ## Check the K3d Cluster Status. Shows a list of K3D clusters and Kubernetes nodes.
	@echo "$(YELLOW)📊 Status k3d cluster:$(NC)"
	k3d cluster list
	@echo "$(YELLOW)📊 Clusters Nodes:$(NC)"
	kubectl get nodes

k3d-clean: ## Delete K3d Cluster
	@echo "$(YELLOW)🗑️ Remove k3d cluster...$(NC)"
	k3d cluster delete $(K3D_CLUSTER)

# === Application ===
app-install: ## Application install
	echo -e "${GREEN}Installing ${BLUE}OWASP Juice Shop ${GREEN}application...${NC}"
	kubectl  apply -f owasp-juiceshop/juice-shop-deployment.yaml

# === debugging ===
shell: ## enter the container
	@echo "$(YELLOW)🐚 Enter the container...$(NC)"
	docker compose -f $(MAIN_COMPOSE) run --rm $(CONTAINER_NAME) bash || true

logs: ## Show Log
	@echo "$(YELLOW)📜 Show container Log:$(NC)"
	docker compose -f $(MAIN_COMPOSE) logs -f $(CONTAINER_NAME)

status: ## show the status of services.
	@echo "$(YELLOW)📊 Status of services:$(NC)"
	@docker compose -f $(MAIN_COMPOSE) ps 2>/dev/null || true
#	@docker compose -f $(ALLURE_COMPOSE) ps 2>/dev/null || true

# === management ===

clean-all: ## complete cleaning (including images). Recommendation: Use carefully
## docker compose ... Down --romi all (deleys the images used by services) and Docker System Prune -f (removes unused Docker objects).
	@echo "$(YELLOW)🧹 Full cleanup (including images)...$(NC)"
	docker compose -f $(MAIN_COMPOSE) down --volumes --remove-orphans --rmi all
	docker compose -f $(ALLURE_COMPOSE) down --volumes --remove-orphans --rmi all
	docker system prune -f
	@make clean

clean: ## cleaning
	@echo "$(YELLOW)🧹 Cleanup...$(NC)"
	sudo rm -rf html-reports/* screenshots/* allure-results/* allure-reports/* logs/*
	sudo find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -name "*.pyc" -delete

# === Allure server management ===
allure-stop: ## allure
	@echo "🛑 Stopping Allure server..."
	docker compose -f $(ALLURE_COMPOSE) down

allure-restart: ## allure
	@echo "🔄 Restart Allure server......"
	docker compose -f $(ALLURE_COMPOSE) restart

allure-start: ## allure
	@echo "🚀 Starting Allure server..."
	docker compose -f $(ALLURE_COMPOSE) --env-file $(ENV_FILE) up -d
	@echo "✅ Allure available: http://localhost:5050/allure/"
	@echo "✅ HTTP available: http://localhost:5050/reports/"
allure-report: ## generate an Allure report from results and open it.
	@echo "$(YELLOW)📈 Generating and opening Allure report...$(NC)"
	@docker compose -f $(ALLURE_COMPOSE) exec -T allure-server sh -c "allure generate --clean allure-results -o allure-report"


#allure-start: ## Starts only Nginx web server to view the report.
#	@echo "🚀 Starting Allure web-server (Nginx) to view reports..."
#	@docker compose -f $(ALLURE_COMPOSE) --env-file $(ENV_FILE) up -d web-server
#	@echo "✅ Allure report available: http://localhost:5050/allure/"
#	@echo "✅ HTTP report available: http://localhost:5050/reports/"
#allure-report: ## generate a new Allure report using the test-runner container, which contain Allure CLI.
#	@echo "$(YELLOW)📈 Running Allure report generation inside test-runner...$(NC)"
#	@docker compose -f $(MAIN_COMPOSE) exec -T $(CONTAINER_NAME) sh -c "allure generate --clean /app/allure-results -o /app/allure-reports"
#	@echo "$(GREEN)✅ Allure report generated in: allure-reports/$(NC)"

# Allure server logs
allure-logs: ## allure
	docker compose -f $(ALLURE_COMPOSE) logs -f