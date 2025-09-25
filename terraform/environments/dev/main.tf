# terraform/environments/dev/main.tf
# Этот файл является корневым модулем.

# Указываем, какие провайдеры будет использовать Terraform
terraform {
  required_providers {
    kubernetes = {
      source = "hashicorp/kubernetes"
      version = "2.23.0"
    }
  }
}

# Настройка провайдера Kubernetes
provider "kubernetes" {
}

# Вызываем наш модуль k6-job
# `source` указывает на локальный путь к модулю
module "k6_test_job" {
  source = "../../modules/k6-job"
  # Сюда можно будет передавать переменные
  # Например:
  # vus = 50
  # duration = "60s"
}