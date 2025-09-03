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

docker-compose up --build