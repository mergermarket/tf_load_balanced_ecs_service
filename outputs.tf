output "name" {
  value = "${element(compact(concat(aws_ecs_service.service.*.name, aws_ecs_service.service_no_loadbalancer.*.name)), 0)}"
}
