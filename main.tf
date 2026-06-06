resource "kubernetes_namespace" "mlops" {
  metadata {
    name = var.namespace
  }
}

resource "kubernetes_deployment" "mlops_app" {
  metadata {
    name      = var.app_name
    namespace = kubernetes_namespace.mlops.metadata[0].name
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        app = var.app_name
      }
    }

    template {
      metadata {
        labels = {
          app = var.app_name
        }
      }

      spec {
        container {
          name  = "mlops-container"
          image = "nginx:latest"
          port {
            container_port = 80
          }
        }
      }
    }
  }
}
