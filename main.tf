resource "aws_ecs_service" "service" {
  name            = "${var.name}"
  cluster         = "${var.cluster}"
  task_definition = "${var.task_definition}"
  desired_count   = "${var.desired_count}"
  iam_role        = "${aws_iam_role.role.arn}"

  load_balancer {
    target_group_arn = "${aws_alb_target_group.target_group.arn}"
    container_name   = "${var.container_name}"
    container_port   = "${var.container_port}"
  }

  placement_strategy {
    type  = "spread"
    field = "attribute:ecs.availability-zone"
  }

  placement_strategy {
    type  = "spread"
    field = "instanceId"
  }
}

resource "aws_alb_target_group" "target_group" {
  name = "${join("", slice(split("", var.name), 0, length(var.name) > 31 ? 31 : length(var.name)))}"

  # port will be set dynamically, but for some reason AWS requires a value
  port                 = "31337"
  protocol             = "HTTP"
  vpc_id               = "${var.vpc_id}"
  deregistration_delay = "${var.deregistration_delay}"

  health_check {
    interval            = "${var.health_check_interval}"
    path                = "${var.health_check_path}"
    timeout             = "${var.health_check_timeout}"
    healthy_threshold   = "${var.health_check_healthy_threshold}"
    unhealthy_threshold = "${var.health_check_unhealthy_threshold}"
    matcher             = "${var.health_check_matcher}"
  }
}

resource "null_resource" "ecs_service_and_target_group" {
  triggers {
    ecs_service_arn = "${aws_ecs_service.service.id}"
    target_group_arn = "${aws_alb_target_group.target_group.arn}"
  }
  depends_on [ "aws_ecs_service.service", "aws_alb_target_group.target_group" ]
}
