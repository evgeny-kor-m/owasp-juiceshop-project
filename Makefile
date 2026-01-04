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
ENV_FILE := .env

-include $(ENV_FILE)
export


# Variables
K3D_CLUSTER = test-lab
IMAGE_NAME = test-runner:latest
CONTAINER_NAME = test-runner


# ========================================================
# 🧭 HELP
# ========================================================
help: ## Show available commands and descriptions
#	@echo "$(BLUE)Available commands:$(NC)"
#	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'
	@echo "$(BLUE)Available commands:$(NC)"
	@grep -hE '^[a-zA-Z0-9_-]+:.*## ' $(MAKEFILE_LIST) \
	| awk 'BEGIN {FS=":.*## "}; {printf "  %-20s %s\n", $$1, $$2}'


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
	@echo "$(BLUE)🚀 Running tests inside container...$(NC)"
	@docker compose -f $(MAIN_COMPOSE) --env-file $(ENV_FILE) up --build

test-report: ## Run tests and generate Allure report
	@echo "$(BLUE)🚀 Running tests and generating Allure report...$(NC)"
	@make clean-all
	@make test
	@make allure-start
	@make allure-report

ci-test: ## Run tests in CI environment (GitHub Actions)
	@echo "$(YELLOW)🚀 Preparing directories for artifacts...$(NC)"
	mkdir -p allure-results allure-reports screenshots html-reports logs
	@echo "$(YELLOW)🚀 Running CI tests with host.docker.internal fix...$(NC)"
	docker run --rm \
		--env-file $(ENV_FILE) \
		--add-host=host.docker.internal:host-gateway \
		-v $$(pwd)/allure-results:/app/allure-results \
		-v $$(pwd)/html-reports:/app/html-reports \
		-v $$(pwd)/logs:/app/logs \
		$(IMAGE_NAME) \
		pytest --alluredir=/app/allure-results \
			   --html=/app/html-reports/report.html \
			   --json-report --json-report-file=/app/html-reports/json_report.json \
			   --cov=test_automation_framework --cov-report=html:/app/html-reports/coverage_html


# ========================================================
# 🧪 LOCAL TESTING (IntelliJ / Host)
# ========================================================

local-test: ## Run pytest locally (for IntelliJ / without Docker)
	@echo "$(BLUE)🧪 Running tests locally with pytest...$(NC)"
	@python3 -m pytest \
		-v \
		--tb=short \
		--alluredir=allure-results

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

k3d-remove: ## Delete K3D cluster completely
	@echo "$(YELLOW)🗑️ Removing K3D cluster $(K3D_CLUSTER)...$(NC)"
	k3d cluster delete $(K3D_CLUSTER)

# ========================================================
# ⚙️ APPLICATION MANAGEMENT
# ========================================================
app-install: ## Deploy test application (OWASP Juice Shop)
	@echo "${GREEN}Installing Ingress Nginx Controller${NC}"
	kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
	@echo "${YELLOW}Waiting for Ingress Nginx Controller to be ready...${NC}"
	kubectl wait --namespace ingress-nginx \
		--for=condition=ready pod \
		--selector=app.kubernetes.io/component=controller \
		--timeout=90s
	@echo "${GREEN}Installing ${BLUE}OWASP Juice Shop ${GREEN}application...${NC}"
	kubectl apply -f owasp-juiceshop/juice-shop-deployment.yaml
	@echo "${GREEN}http://juice-shop.local:8080/ - Juice Shop application${NC}"

# ========================================================
# 🧩 DEBUGGING
# ========================================================
shell: ## Enter container shell (interactive bash)
	@echo "$(YELLOW)🐚 Entering container shell...$(NC)"
	docker compose -f $(MAIN_COMPOSE) --env-file $(ENV_FILE) run --rm $(CONTAINER_NAME) bash || true

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
	sudo rm -rf $(HTML_REPORTS_DIR) $(SCREENSHOTS_DIR) $(ALLURE_RESULTS_DIR) $(ALLURE_REPORTS_DIR) $(LOGS_DIR) || true

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
	@docker compose -f $(ALLURE_COMPOSE) --env-file $(ENV_FILE) exec -T allure-server sh -c "allure generate --clean allure-results -o allure-report"
	@echo "$(GREEN)✅ Report generated!$(NC)"
	@echo "$(YELLOW)🌐 Opening Allure report at http://localhost:$(ALLURE_PORT)/allure/ ...$(NC)"
	-@if [ "$$(uname -r | grep -i microsoft)" ]; then \
		if command -v explorer.exe > /dev/null; then \
			explorer.exe "http://localhost:$(ALLURE_PORT)/allure/" || true; \
		elif [ -f "/mnt/c/Windows/explorer.exe" ]; then \
			/mnt/c/Windows/explorer.exe "http://localhost:$(ALLURE_PORT)/allure/" || true; \
		elif command -v powershell.exe > /dev/null; then \
			powershell.exe -Command "Start-Process 'http://localhost:$(ALLURE_PORT)/allure/'" || true; \
		else \
			echo "$(RED)⚠️ WSL: explorer.exe and powershell.exe not found in PATH.$(NC)"; \
		fi; \
	elif [ "$$(uname)" = "Darwin" ]; then \
		open "http://localhost:$(ALLURE_PORT)/allure/" || true; \
	elif command -v xdg-open > /dev/null; then \
		xdg-open "http://localhost:$(ALLURE_PORT)/allure/" || true; \
	else \
		echo "$(YELLOW)ℹ️ Please open manually: http://localhost:$(ALLURE_PORT)/allure/$(NC)"; \
	fi

