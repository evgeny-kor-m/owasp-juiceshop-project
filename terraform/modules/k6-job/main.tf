# terraform/modules/k6-job/main.tf

# Указываем, какие провайдеры будет использовать Terraform
# В данном случае, это провайдер Kubernetes
terraform {
  required_providers {
    kubernetes = {
      source = "hashicorp/kubernetes"
      version = "2.23.0" # Используйте актуальную версию
    }
  }
}

# Настройка провайдера Kubernetes
# Terraform автоматически использует конфигурацию `kubectl`,
# поэтому здесь достаточно пустой секции
provider "kubernetes" {
}

# Ресурс 1: Создаем пространство имен для тестов k6
resource "kubernetes_namespace_v1" "k6_tests_namespace" {
  metadata {
    name = "k6-tests"
  }
}

# Ресурс 2: Создаем ConfigMap для нашего k6-скрипта
# `depends_on` гарантирует, что namespace будет создан первым
resource "kubernetes_config_map_v1" "k6_script_configmap" {
  metadata {
    name = "k6-test-script"
    namespace = kubernetes_namespace_v1.k6_tests_namespace.metadata[0].name
  }

  data = {
    # Здесь мы определяем наш скрипт.
    "test-script.js" = <<-EOT
      import http from 'k6/http';
      import { sleep } from 'k6';

      export const options = {
        vus: 10,  // 10 виртуальных пользователей
        duration: '30s', // Длительность теста - 30 секунд
      };

      export default function () {
        http.get('http://juice-shop.local');
        sleep(1);
      }
    EOT
  }
}

# Ресурс 3: Создаем Job, который запустит k6 тест
resource "kubernetes_job_v1" "k6_test_job" {
  metadata {
    name = "k6-test-job"
    namespace = kubernetes_namespace_v1.k6_tests_namespace.metadata[0].name
  }

  spec {
    template {
      metadata {} # Пустой блок metadata
      spec {
        service_account_name = "default"
        container {
          name = "k6"
          image = "grafana/k6:latest" # Используем официальный образ k6
          args = ["run", "/scripts/test-script.js"]
          volume_mount {
            name = "k6-script-volume"
            mount_path = "/scripts"
          }
        }
        restart_policy = "Never"
        volume {
          name = "k6-script-volume"
          config_map {
            name = kubernetes_config_map_v1.k6_script_configmap.metadata[0].name
          }
        }
      }
    }
    backoff_limit = 0 # Не перезапускаем Job при ошибке
  }
}