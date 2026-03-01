# ==============================================================================
# TERRAFORM
# ==============================================================================

terraform {
  required_version = ">= 1.14.0"

  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 3.0.1"
    }
  }
}


# ==============================================================================
# VARIABLES
# ==============================================================================

variable "kubernetes_namespace" {
  description = "Kubernetes namespace."
  default     = "backend"
  type        = string
}

variable "image_repository" {
  description = "Container image repository."
  default     = "ghcr.io/thmb/backend"
  type        = string
}

variable "image_tag" {
  description = "Container image tag."
  default     = "latest"
  type        = string
}

variable "deployment_replicas" {
  description = "Number of backend pod replicas."
  default     = 1
  type        = number
}

variable "ingress_host" {
  description = "Ingress hostname for the API."
  default     = "api.localhost"
  type        = string
}

variable "database_host" {
  description = "PostgreSQL database host."
  type        = string
}

variable "database_port" {
  description = "PostgreSQL database port."
  default     = 5432
  type        = number
}

variable "database_name" {
  description = "PostgreSQL database name."
  default     = "application"
  type        = string
}

variable "database_user" {
  description = "PostgreSQL database user."
  default     = "backend"
  type        = string
}

variable "database_password" {
  description = "PostgreSQL database password."
  type        = string
  sensitive   = true
}


# ==============================================================================
# LOCALS
# ==============================================================================

locals {
  app_name = "backend"

  labels = {
    app       = local.app_name
    component = "api"
    managedBy = "terraform"
  }
}


# ==============================================================================
# NAMESPACE
# ==============================================================================

resource "kubernetes_namespace_v1" "backend" {
  metadata {
    name = var.kubernetes_namespace
    labels = {
      name = var.kubernetes_namespace
    }
  }
}


# ==============================================================================
# SECRET
# ==============================================================================

resource "kubernetes_secret_v1" "backend" {
  metadata {
    name      = "${local.app_name}-secret"
    namespace = kubernetes_namespace_v1.backend.metadata[0].name
    labels    = local.labels
  }

  data = {
    DATABASE_PASSWORD = var.database_password
  }

  type = "Opaque"
}


# ==============================================================================
# CONFIGMAP
# ==============================================================================

resource "kubernetes_config_map_v1" "backend" {
  metadata {
    name      = "${local.app_name}-config"
    namespace = kubernetes_namespace_v1.backend.metadata[0].name
    labels    = local.labels
  }

  data = {
    DATABASE_HOST = var.database_host
    DATABASE_PORT = tostring(var.database_port)
    DATABASE_NAME = var.database_name
    DATABASE_USER = var.database_user
    ENVIRONMENT   = "production"
    DEBUG         = "false"
  }
}


# ==============================================================================
# DEPLOYMENT
# ==============================================================================

resource "kubernetes_deployment_v1" "backend" {
  metadata {
    name      = local.app_name
    namespace = kubernetes_namespace_v1.backend.metadata[0].name
    labels    = local.labels
  }

  spec {
    replicas = var.deployment_replicas

    selector {
      match_labels = {
        app = local.app_name
      }
    }

    template {
      metadata {
        labels = local.labels
      }

      spec {
        container {
          name              = local.app_name
          image             = "${var.image_repository}:${var.image_tag}"
          image_pull_policy = var.image_tag == "latest" ? "Always" : "IfNotPresent"

          port {
            container_port = 8000
            protocol       = "TCP"
          }

          env_from {
            config_map_ref {
              name = kubernetes_config_map_v1.backend.metadata[0].name
            }
          }

          env_from {
            secret_ref {
              name = kubernetes_secret_v1.backend.metadata[0].name
            }
          }

          resources {
            requests = {
              cpu    = "100m"
              memory = "256Mi"
            }
            limits = {
              cpu    = "500m"
              memory = "512Mi"
            }
          }

          liveness_probe {
            http_get {
              path = "/health"
              port = 8000
            }
            initial_delay_seconds = 10
            period_seconds        = 30
            timeout_seconds       = 5
            failure_threshold     = 3
          }

          readiness_probe {
            http_get {
              path = "/health"
              port = 8000
            }
            initial_delay_seconds = 5
            period_seconds        = 10
            timeout_seconds       = 3
            failure_threshold     = 3
          }
        }
      }
    }
  }
}


# ==============================================================================
# SERVICE
# ==============================================================================

resource "kubernetes_service_v1" "backend" {
  metadata {
    name      = local.app_name
    namespace = kubernetes_namespace_v1.backend.metadata[0].name
    labels    = local.labels
  }

  spec {
    selector = {
      app = local.app_name
    }

    port {
      name        = "http"
      port        = 80
      target_port = 8000
      protocol    = "TCP"
    }

    type = "ClusterIP"
  }
}


# ==============================================================================
# INGRESS
# ==============================================================================

resource "kubernetes_ingress_v1" "backend" {
  metadata {
    name      = local.app_name
    namespace = kubernetes_namespace_v1.backend.metadata[0].name
    labels    = local.labels
    annotations = {
      "traefik.ingress.kubernetes.io/router.entrypoints" = "web"
    }
  }

  spec {
    ingress_class_name = "traefik"

    rule {
      host = var.ingress_host

      http {
        path {
          path      = "/"
          path_type = "Prefix"

          backend {
            service {
              name = kubernetes_service_v1.backend.metadata[0].name
              port { name = "http" }
            }
          }
        }
      }
    }
  }
}


# ==============================================================================
# OUTPUTS
# ==============================================================================

output "service_endpoint" {
  description = "Kubernetes service endpoint."
  value       = "http://${kubernetes_service_v1.backend.metadata[0].name}.${kubernetes_namespace_v1.backend.metadata[0].name}.svc.cluster.local"
}

output "health_endpoint" {
  description = "Health check endpoint."
  value       = "http://${var.ingress_host}/health"
}

output "docs_endpoint" {
  description = "API documentation endpoint."
  value       = "http://${var.ingress_host}/docs"
}
