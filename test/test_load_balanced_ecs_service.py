import re
import unittest
import os
import time
from textwrap import dedent
from subprocess import check_call, check_output

cwd = os.getcwd()


def _terraform_escape_value(value):
    def escape(match):
        return '\\n' if match.group(0) == '\n' else '\\"'
    return re.sub(r'([\n"])', escape, value)

class TestCreateTaskdef(unittest.TestCase):

    def setUp(self):
        check_call([ 'terraform', 'init', 'test/infra' ])


    def test_create_target_group(self):
        output = check_output([
            'terraform',
            'plan',
            '-no-color',
            '-target=module.target_group',
            'test/infra'
        ]).decode('utf-8')

        assert dedent("""
            + module.target_group.aws_alb_target_group.target_group
                  id:                                         <computed>
                  arn:                                        <computed>
                  arn_suffix:                                 <computed>
                  deregistration_delay:                       "10"
                  health_check.#:                             "1"
                  health_check.0.healthy_threshold:           "2"
                  health_check.0.interval:                    "5"
                  health_check.0.matcher:                     "200-299"
                  health_check.0.path:                        "/internal/healthcheck"
                  health_check.0.port:                        "traffic-port"
                  health_check.0.protocol:                    "HTTP"
                  health_check.0.timeout:                     "4"
                  health_check.0.unhealthy_threshold:         "2"
                  name:                                       "test-service"
                  port:                                       "31337"
                  protocol:                                   "HTTP"
                  proxy_protocol_v2:                          "false"
                  slow_start:                                 "0"
                  stickiness.#:                               <computed>
                  target_type:                                "instance"
                  vpc_id:                                     "test-vpc"
        """).strip() in output

    def test_create_ecs_service(self):
        output = check_output([
            'terraform',
            'plan',
            '-no-color',
            '-target=module.service',
            'test/infra'
        ]).decode('utf-8')
        assert dedent("""
            + module.service.aws_ecs_service.service
                  id:                                         <computed>
                  cluster:                                    "default"
                  deployment_maximum_percent:                 "200"
                  deployment_minimum_healthy_percent:         "100"
                  desired_count:                              "3"
                  enable_ecs_managed_tags:                    "false"
                  iam_role:                                   "${aws_iam_role.role.arn}"
                  launch_type:                                "EC2"
                  load_balancer.#:                            "1"
                  load_balancer.~2788651468.container_name:   "app"
                  load_balancer.~2788651468.container_port:   "8000"
                  load_balancer.~2788651468.elb_name:         ""
                  load_balancer.~2788651468.target_group_arn: "${aws_alb_target_group.target_group.arn}"
                  name:                                       "test-service"
                  ordered_placement_strategy.#:               "2"
                  ordered_placement_strategy.0.field:         "attribute:ecs.availability-zone"
                  ordered_placement_strategy.0.type:          "spread"
                  ordered_placement_strategy.1.field:         "instanceId"
                  ordered_placement_strategy.1.type:          "spread"
                  platform_version:                           <computed>
                  scheduling_strategy:                        "REPLICA"
                  task_definition:                            "test-taskdef"
        """).strip() in output



    def test_create_role(self):
        output = check_output([
            'terraform',
            'plan',
            '-no-color',
            '-target=module.role',
            'test/infra'
        ]).decode('utf-8')

        expected_assume_role_policy_doc = dedent("""
            {
              "Version": "2012-10-17",
              "Statement": [
                {
                  "Action": "sts:AssumeRole",
                  "Principal": { "Service": "ecs.amazonaws.com" },
                  "Effect": "Allow"
                }
              ]
            }
        """).strip() + "\n"

        assert dedent("""
            + module.role.aws_iam_role.role
                  id:                                         <computed>
                  arn:                                        <computed>
                  assume_role_policy:                         "{assume_role_policy}"
                  create_date:                                <computed>
                  force_detach_policies:                      "false"
                  max_session_duration:                       "3600"
                  name:                                       <computed>
                  name_prefix:                                "test-service"
                  path:                                       "/"
                  unique_id:                                  <computed>
        """).strip().format(assume_role_policy=_terraform_escape_value(
            expected_assume_role_policy_doc
        )) in output

        # assert expected_role_plan in output.replace(" ", "")

    def test_create_service_with_long_name(self):
        output = check_output([
            'terraform',
            'plan',
            '-no-color',
            '-target=module.service_with_long_name',
            'test/infra'
        ]).decode('utf-8')

        expected_assume_role_policy_doc = dedent("""
            {
              "Version": "2012-10-17",
              "Statement": [
                {
                  "Action": "sts:AssumeRole",
                  "Principal": { "Service": "ecs.amazonaws.com" },
                  "Effect": "Allow"
                }
              ]
            }
        """).strip() + "\n"

        assert dedent("""
            + module.service_with_long_name.aws_iam_role.role
                  id:                                         <computed>
                  arn:                                        <computed>
                  assume_role_policy:                         "{assume_role_policy}"
                  create_date:                                <computed>
                  force_detach_policies:                      "false"
                  max_session_duration:                       "3600"
                  name:                                       <computed>
                  name_prefix:                                "test-service-humptydumptysatona"
                  path:                                       "/"
                  unique_id:                                  <computed>
        """).strip().format(assume_role_policy=_terraform_escape_value(
            expected_assume_role_policy_doc
        )) in output

        assert dedent("""
            + module.service_with_long_name.aws_iam_role_policy.policy
                  id:                                         <computed>
                  name:                                       <computed>
                  name_prefix:                                "test-service-humptydumptysatona"
        """).strip() in output

        assert dedent("""
            + module.service_with_long_name.aws_ecs_service.service
                  id:                                         <computed>
                  cluster:                                    "default"
                  deployment_maximum_percent:                 "200"
                  deployment_minimum_healthy_percent:         "100"
                  desired_count:                              "3"
                  enable_ecs_managed_tags:                    "false"
                  iam_role:                                   "${aws_iam_role.role.arn}"
                  launch_type:                                "EC2"
                  load_balancer.#:                            "1"
                  load_balancer.~2788651468.container_name:   "app"
                  load_balancer.~2788651468.container_port:   "8000"
                  load_balancer.~2788651468.elb_name:         ""
                  load_balancer.~2788651468.target_group_arn: "${aws_alb_target_group.target_group.arn}"
                  name:                                       "test-service-humptydumptysatonawallhumptydumptyhadagreatfall"
        """).strip() in output

        assert dedent("""
            + module.service_with_long_name.aws_alb_target_group.target_group
                  id:                                         <computed>
                  arn:                                        <computed>
                  arn_suffix:                                 <computed>
                  deregistration_delay:                       "10"
                  health_check.#:                             "1"
                  health_check.0.healthy_threshold:           "2"
                  health_check.0.interval:                    "5"
                  health_check.0.matcher:                     "200-299"
                  health_check.0.path:                        "/internal/healthcheck"
                  health_check.0.port:                        "traffic-port"
                  health_check.0.protocol:                    "HTTP"
                  health_check.0.timeout:                     "4"
                  health_check.0.unhealthy_threshold:         "2"
                  name:                                       "test-service-humptydumptysatonaw"
        """).strip() in output

    def test_create_policy(self):
        output = check_output([
            'terraform',
            'plan',
            '-no-color',
            '-target=module.policy',
            'test/infra'
        ]).decode('utf-8')

        expected_service_policy_doc = dedent("""
            {
              "Version": "2012-10-17",
              "Statement": [
                {
                  "Effect": "Allow",
                  "Action": [
                    "ec2:AuthorizeSecurityGroupIngress",
                    "ec2:Describe*",
                    "elasticloadbalancing:DeregisterInstancesFromLoadBalancer",
                    "elasticloadbalancing:DeregisterTargets",
                    "elasticloadbalancing:Describe*",
                    "elasticloadbalancing:RegisterInstancesWithLoadBalancer",
                    "elasticloadbalancing:RegisterTargets"
                  ],
                  "Resource": "*"
                }
              ]
            }
        """).strip() + "\n"
 
        assert dedent("""
            + module.policy.aws_iam_role_policy.policy
                  id:                                         <computed>
                  name:                                       <computed>
                  name_prefix:                                "test-service"
                  policy:                                     "{service_policy_doc}"
                  role:                                       "${{aws_iam_role.role.id}}"
        """).strip().format(service_policy_doc=_terraform_escape_value(
            expected_service_policy_doc
        )) in output

    def test_correct_number_of_resources(self):
        output = check_output([
            'terraform',
            'plan',
            '-no-color',
            '-target=module.all',
            'test/infra'
        ]).decode('utf-8')
        assert "Plan: 6 to add, 0 to change, 0 to destroy." in output
