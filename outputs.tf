output "target_group_arn" {
  value = "${aws_alb_target_group.target_group.arn}"
  description = "The ARN of the target group for use by ALB listener rules (e.g. as a parameter to the tf_alb_listener_rules module: https://github.com/mergermarket/tf_alb_listener_rules)."
}
