output "target_group_arn" {
  value = "${null_resource.ecs_service_and_target_group.triggers.target_group_arn}"
  description = "The ARN of the target group for use by ALB listener rules (e.g. as a parameter to the tf_alb_listener_rules module: https://github.com/mergermarket/tf_alb_listener_rules)."
}
