resource "aws_ecs_service" "service" {
  count = "${var.target_group_arn != "" ? 1 : 0}"

  name                               = "${var.name}"
  cluster                            = "${var.cluster}"
  task_definition                    = "${var.task_definition}"
  desired_count                      = "${var.desired_count}"
  iam_role                           = "${aws_iam_role.role.arn}"
  deployment_minimum_healthy_percent = "${var.deployment_minimum_healthy_percent}"
  deployment_maximum_percent         = "${var.deployment_maximum_percent}"
  tags                               = "${var.tags}"
  health_check_grace_period_seconds  = "${var.health_check_grace_period_seconds}"

  load_balancer {
    target_group_arn = "${var.target_group_arn}"
    container_name   = "${var.container_name}"
    container_port   = "${var.container_port}"
  }

  ordered_placement_strategy {
    type  = "spread"
    field = "attribute:ecs.availability-zone"
  }

  ordered_placement_strategy {
    type  = "spread"
    field = "instanceId"
  }
  
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_ecs_service" "service_no_loadbalancer" {
  count = "${var.target_group_arn == "" ? 1 : 0}"

  name                               = "${var.name}"
  cluster                            = "${var.cluster}"
  task_definition                    = "${var.task_definition}"
  desired_count                      = "${var.desired_count}"
  deployment_minimum_healthy_percent = "${var.deployment_minimum_healthy_percent}"
  deployment_maximum_percent         = "${var.deployment_maximum_percent}"
  tags                               = "${var.tags}"
  health_check_grace_period_seconds  = "${var.health_check_grace_period_seconds}"

  ordered_placement_strategy {
    type  = "spread"
    field = "attribute:ecs.availability-zone"
  }

  ordered_placement_strategy {
    type  = "spread"
    field = "instanceId"
  }
}
