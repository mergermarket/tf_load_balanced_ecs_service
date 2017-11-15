# Required parameters

variable "name" {
  description = "Name/name prefix to apply to the resources in the module."
  type        = "string"
}

variable "vpc_id" {
  description = "The identifier of the VPC in which to create the target group."
  type        = "string"
}

variable "task_definition" {
  description = "The family and revision (family:revision) or full ARN of the task definition that you want to run in your service."
  type        = "string"
}

variable "target_group_arn" {
  description = "The target group ARN"
  type        = "string"
}

# Optional parameters

variable "cluster" {
  description = "The name of the ECS cluster to deploy the service to."
  type        = "string"
  default     = "default"
}

variable "desired_count" {
  description = "The number of instances of the task definition to place and keep running."
  type        = "string"
  default     = "3"
}

variable "container_name" {
  description = "The name of the container to associate with the load balancer (as it appears in a container definition)."
  type        = "string"
  default     = "app"
}

variable "container_port" {
  description = "The port on the container to associate with the load balancer."
  type        = "string"
  default     = "8000"
}

variable "deregistration_delay" {
  description = "The amount time for Elastic Load Balancing to wait before changing the state of a deregistering target from draining to unused. The range is 0-3600 seconds."
  type        = "string"
  default     = "10"
}

variable "health_check_interval" {
  description = "The approximate amount of time, in seconds, between health checks of an individual target. Minimum value 5 seconds, Maximum value 300 seconds."
  type        = "string"
  default     = "5"
}

variable "health_check_path" {
  description = "The destination for the health check request."
  type        = "string"
  default     = "/internal/healthcheck"
}

variable "health_check_timeout" {
  description = "The amount of time, in seconds, during which no response means a failed health check."
  type        = "string"
  default     = "4"
}

variable "health_check_healthy_threshold" {
  description = "The number of consecutive health checks successes required before considering an unhealthy target healthy."
  type        = "string"
  default     = "2"
}

variable "health_check_unhealthy_threshold" {
  description = "The number of consecutive health check failures required before considering the target unhealthy."
  type        = "string"
  default     = "2"
}

variable "health_check_matcher" {
  description = "The HTTP codes to use when checking for a successful response from a target. You can specify multiple values (for example, \"200,202\") or a range of values (for example, \"200-299\")."
  type        = "string"
  default     = "200-299"
}

variable "alb_listener_arn" {
  description = "We need this to be available before the service can be created"
  default     = ""
}

variable "alb_arn" {
  description = "The ARN of the ALB (used to ensure the ALB exists before the target group is associated with the service, since otherwise it fails)."
  default     = ""
}
