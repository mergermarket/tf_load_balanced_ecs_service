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
        check_call([ 'terraform', 'get', 'test/infra' ])


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
                arn:                                "<computed>"
                arn_suffix:                         "<computed>"
                deregistration_delay:               "10"
                health_check.#:                     "1"
                health_check.0.healthy_threshold:   "2"
                health_check.0.interval:            "5"
                health_check.0.matcher:             "200-299"
                health_check.0.path:                "/internal/healthcheck"
                health_check.0.port:                "traffic-port"
                health_check.0.protocol:            "HTTP"
                health_check.0.timeout:             "4"
                health_check.0.unhealthy_threshold: "2"
                name:                               "test-service"
                port:                               "31337"
                protocol:                           "HTTP"
                stickiness.#:                       "<computed>"
                vpc_id:                             "test-vpc"
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
                cluster:                                    "default"
                deployment_maximum_percent:                 "200"
                deployment_minimum_healthy_percent:         "100"
                desired_count:                              "3"
                iam_role:                                   "${aws_iam_role.role.arn}"
                load_balancer.#:                            "1"
                load_balancer.~2788651468.container_name:   "app"
                load_balancer.~2788651468.container_port:   "8000"
                load_balancer.~2788651468.elb_name:         ""
                load_balancer.~2788651468.target_group_arn: "${aws_alb_target_group.target_group.arn}"
                name:                                       "test-service"
                placement_strategy.#:                       "2"
                placement_strategy.2093792364.field:        "attribute:ecs.availability-zone"
                placement_strategy.2093792364.type:         "spread"
                placement_strategy.3946258308.field:        "instanceId"
                placement_strategy.3946258308.type:         "spread"
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

        expected_role_plan = dedent("""
            + module.role.aws_iam_role.role
                arn:                "<computed>"
                assume_role_policy: "{assume_role_policy}"
                create_date:        "<computed>"
                name:               "<computed>"
                name_prefix:        "test-service"
                path:               "/"
                unique_id:          "<computed>"
        """).strip().format(assume_role_policy=_terraform_escape_value(
            expected_assume_role_policy_doc
        ))
        assert expected_role_plan in output

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

        expected_role_plan = dedent("""
            + module.service_with_long_name.aws_iam_role.role
                arn:                "<computed>"
                assume_role_policy: "{assume_role_policy}"
                create_date:        "<computed>"
                name:               "<computed>"
                name_prefix:        "test-service-humptydumptysatona"
                path:               "/"
                unique_id:          "<computed>"
        """).strip().format(assume_role_policy=_terraform_escape_value(
            expected_assume_role_policy_doc
        ))
        expected_role_policy_plan = dedent("""
            + module.service_with_long_name.aws_iam_role_policy.policy
                name:        "<computed>"
                name_prefix: "test-service-humptydumptysatona"
        """).strip()
        expected_aws_ecs_service_plan = dedent("""
            + module.service_with_long_name.aws_ecs_service.service
                cluster:                                    "default"
                deployment_maximum_percent:                 "200"
                deployment_minimum_healthy_percent:         "100"
                desired_count:                              "3"
                iam_role:                                   "${aws_iam_role.role.arn}"
                load_balancer.#:                            "1"
                load_balancer.~2788651468.container_name:   "app"
                load_balancer.~2788651468.container_port:   "8000"
                load_balancer.~2788651468.elb_name:         ""
                load_balancer.~2788651468.target_group_arn: "${aws_alb_target_group.target_group.arn}"
                name:                                       "test-service-humptydumptysatonawallhumptydumptyhadagreatfall"
        """).strip() # noqa
        expected_aws_alb_target_group_plan = dedent("""
            + module.service_with_long_name.aws_alb_target_group.target_group
                arn:                                "<computed>"
                arn_suffix:                         "<computed>"
                deregistration_delay:               "10"
                health_check.#:                     "1"
                health_check.0.healthy_threshold:   "2"
                health_check.0.interval:            "5"
                health_check.0.matcher:             "200-299"
                health_check.0.path:                "/internal/healthcheck"
                health_check.0.port:                "traffic-port"
                health_check.0.protocol:            "HTTP"
                health_check.0.timeout:             "4"
                health_check.0.unhealthy_threshold: "2"
                name:                               "test-service-humptydumptysatona"
        """).strip() # noqa

        assert expected_role_plan in output
        assert expected_role_policy_plan in output
        assert expected_aws_ecs_service_plan in output
        assert expected_aws_alb_target_group_plan in output

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
                name:        "<computed>"
                name_prefix: "test-service"
                policy:      "{service_policy_doc}"
                role:        "${{aws_iam_role.role.id}}"
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
