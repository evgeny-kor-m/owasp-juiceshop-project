# main.tf

# Указываем необходимые провайдеры
terraform {
  required_providers {
    kubernetes = {
      source = "hashicorp/kubernetes"
      version = "2.23.0"
    }
    helm = {
      source = "hashicorp/helm"
      version = "2.12.1"
    }
  }
}

# Настройка провайдера Kubernetes
provider "kubernetes" {}

# Настройка провайдера Helm
provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}

# --- Установка Ingress-контроллера Nginx ---
resource "helm_release" "nginx_ingress" {
  name = "nginx-ingress"
  repository = "https://kubernetes.github.io/ingress-nginx"
  chart = "ingress-nginx"
  namespace = "ingress-nginx"
  create_namespace = true
}

# --- Установка Prometheus и Grafana с помощью kube-prometheus-stack ---
resource "helm_release" "monitoring" {
  name = "kube-prometheus-stack"
  repository = "https://prometheus-community.github.io/helm-charts"
  chart = "kube-prometheus-stack"
  namespace = "monitoring"
  create_namespace = true

  # Зависимость от установки Ingress-контроллера
  depends_on = [helm_release.nginx_ingress]

  # Переопределение значений Helm-чарта
  # Этот блок можно расширить, чтобы настроить Ingress для Grafana
  values = [
    <<-EOT
      grafana:
        ingress:
          enabled: true
          # Укажите желаемый хост для Grafana
          hosts:
            - grafana.juice-shop.local
          path: /
          pathType: Prefix
          # Убедитесь, что ingress_class соответствует Ingress-контроллеру
          ingressClassName: "nginx"
          annotations:
            kubernetes.io/tls-acme: "true"
            cert-manager.io/cluster-issuer: "letsencrypt-staging"
    EOT
  ]
}

# Ресурс 3: Создание Ingress-ресурса для Juice Shop
# Обратите внимание, что вы можете создать этот ресурс отдельно
# Если вы уже установили Ingress-контроллер
resource "kubernetes_ingress_v1" "juice_shop_ingress" {
  metadata {
    name = "juice-shop-ingress"
    namespace = "test-automation"
    annotations = {
      "kubernetes.io/ingress.class" = "nginx"
    }
  }
  spec {
    ingress_class_name = "nginx"
    rule {
      host = "juice-shop.local"
      http {
        path {
          path = "/"
          path_type = "Prefix"
          backend {
            service {
              name = "juice-shop-service"
              port {
                number = 80
              }
            }
          }
        }
      }
    }
  }
}