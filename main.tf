resource "aws_ecs_service" "service" {
  name            = "${var.name}"
  cluster         = "${var.cluster}"
  task_definition = "${var.task_definition}"
  desired_count   = "${var.desired_count}"
  iam_role        = "${aws_iam_role.role.arn}"

  load_balancer {
    target_group_arn = "${var.target_group_arn}"
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

  depends_on = ["null_resource.alb_listener_arn", "null_resource.alb_arn"]
}

resource "null_resource" "alb_listener_arn" {
  triggers {
    alb_listener_arn = "${var.alb_listener_arn}"
  }
}

resource "null_resource" "alb_arn" {
  triggers {
    alb_name = "${var.alb_arn}"
  }
}
