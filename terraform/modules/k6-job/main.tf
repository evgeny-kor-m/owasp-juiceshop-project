# terraform/modules/k6-job/main.tf
# Этот файл является модулем. Он не содержит `provider` или `terraform` блоки.

# Ресурс 1: Создаем пространство имен для тестов k6
resource "kubernetes_namespace_v1" "k6_tests_namespace" {
  metadata {
    name = "k6-tests"
  }
}

# Ресурс 2: Создаем ConfigMap для нашего k6-скрипта
resource "kubernetes_config_map_v1" "k6_script_configmap" {
  metadata {
    name = "k6-test-script"
    namespace = kubernetes_namespace_v1.k6_tests_namespace.metadata[0].name
  }

  data = {
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
      metadata {}
      spec {
        service_account_name = "default"
        container {
          name = "k6"
          image = "grafana/k6:latest"
          args = ["run", "/scripts/test-script.js"]
          volume_mount {
            name = "k6-script"
            mount_path = "/scripts"
            read_only = true
          }
        }
        volume {
          name = "k6-script"
          config_map {
            name = kubernetes_config_map_v1.k6_script_configmap.metadata[0].name
          }
        }
        restart_policy = "OnFailure"
      }
    }
  }
}