variable "namespace" {
  description = "Kubernetes namespace for deployment"
  type        = string
  default     = "mlops"
}

variable "replicas" {
  description = "Number of pod replicas"
  type        = number
  default     = 3
}

variable "app_name" {
  description = "Application name"
  type        = string
  default     = "mlops-app"
}
