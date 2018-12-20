import re
import unittest
import os
from textwrap import dedent
from subprocess import check_call, check_output

cwd = os.getcwd()


def _terraform_escape_value(value):
    def escape(match):
        return '\\n' if match.group(0) == '\n' else '\\"'
    return re.sub(r'([\n"])', escape, value)


class TestCreateTaskdef(unittest.TestCase):

    def setUp(self):
        check_call(['terraform', 'get', 'test/infra'])
        check_call(['terraform', 'init', 'test/infra'])

    def test_create_ecs_service(self):
        output = check_output([
            'terraform',
            'plan',
            '-no-color',
            '-target=module.service',
            'test/infra'
        ]).decode('utf-8')

        expected_service = dedent("""
+ module.service.aws_ecs_service.service
      id:                                      <computed>
      cluster:                                 "default"
      deployment_maximum_percent:              "200"
      deployment_minimum_healthy_percent:      "100"
      desired_count:                           "3"
      enable_ecs_managed_tags:                 "false"
      iam_role:                                "${aws_iam_role.role.arn}"
      launch_type:                             "EC2"
      load_balancer.#:                         "1"
      load_balancer.53344424.container_name:   "app"
      load_balancer.53344424.container_port:   "8000"
      load_balancer.53344424.elb_name:         ""
      load_balancer.53344424.target_group_arn: "some-target-group-arn"
      name:                                    "test-service"
      ordered_placement_strategy.#:            "2"
      ordered_placement_strategy.0.field:      "attribute:ecs.availability-zone"
      ordered_placement_strategy.0.type:       "spread"
      ordered_placement_strategy.1.field:      "instanceId"
      ordered_placement_strategy.1.type:       "spread"
      scheduling_strategy:                     "REPLICA"
      task_definition:                         "test-taskdef"
        """)

        assert expected_service.replace(" ", "") in output.replace(" ", "")

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
                id:                                      <computed>
                arn:                                     <computed>
                assume_role_policy:                      "{assume_role_policy}"
                create_date:                             <computed>
                force_detach_policies:                   "false"
                max_session_duration:                    "3600"
                name:                                    <computed>
                name_prefix:                             "test-service"
                path:                                    "/"
                unique_id:                               <computed>
        """).strip().format(
                assume_role_policy=_terraform_escape_value(
                    expected_assume_role_policy_doc
                )
            )
        assert expected_role_plan.replace(" ", "") in output.replace(" ", "")

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
              id:                                      <computed>
              arn:                                     <computed>
              assume_role_policy:                      "{assume_role_policy}"
              create_date:                             <computed>
              force_detach_policies:                   "false"
              max_session_duration:                    "3600"
              name:                                    <computed>
              name_prefix:                             "test-service-humptydumptysatona"
              path:                                    "/"
              unique_id:                               <computed>
        """).strip().format(assume_role_policy=_terraform_escape_value(
            expected_assume_role_policy_doc
        ))
        expected_role_policy_plan = dedent("""
          + module.service_with_long_name.aws_iam_role_policy.policy
              id:                                      <computed>
              name:                                    <computed>
              name_prefix:                             "test-service-humptydumptysatona"
        """).strip()
        expected_aws_ecs_service_plan = dedent("""
            + module.service_with_long_name.aws_ecs_service.service
                  id:                                      <computed>
                  cluster:                                 "default"
                  deployment_maximum_percent:              "200"
                  deployment_minimum_healthy_percent:      "100"
                  desired_count:                           "3"
                  enable_ecs_managed_tags:                 "false"
                  iam_role:                                "${aws_iam_role.role.arn}"
                  launch_type:                             "EC2"
                  load_balancer.#:                         "1"
                  load_balancer.53344424.container_name:   "app"
                  load_balancer.53344424.container_port:   "8000"
                  load_balancer.53344424.elb_name:         ""
                  load_balancer.53344424.target_group_arn: "some-target-group-arn"
                  name:                                    "test-service-humptydumptysatonawallhumptydumptyhadagreatfall"
                  ordered_placement_strategy.#:            "2"
                  ordered_placement_strategy.0.field:      "attribute:ecs.availability-zone"
                  ordered_placement_strategy.0.type:       "spread"
                  ordered_placement_strategy.1.field:      "instanceId"
                  ordered_placement_strategy.1.type:       "spread"
                  scheduling_strategy:                     "REPLICA"
                  task_definition:                         "test-taskdef"
        """).strip() # noqa

        assert expected_role_plan.replace(" ", "") in output.replace(" ", "")
        assert expected_role_policy_plan.replace(" ", "") in output.replace(" ", "")
        assert expected_aws_ecs_service_plan.replace(" ", "") in output.replace(" ", "")

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

        expected_policy = dedent("""
  + module.policy.aws_iam_role_policy.policy
      id:                                      <computed>
      name:                                    <computed>
      name_prefix:                             "test-service"
      policy:                                  "{service_policy_doc}"
        """).strip().format(service_policy_doc=_terraform_escape_value(
            expected_service_policy_doc
        ))
        assert expected_policy.replace(" ", "") in output.replace(" ", "")

    def test_min_and_max_perecent(self):
        output = check_output([
            'terraform',
            'plan',
            '-no-color',
            '-target=module.service_with_custom_min_and_max_perecent',
            'test/infra'
        ]).decode('utf-8')

        expected_plan = dedent("""
           + module.service_with_custom_min_and_max_perecent.aws_ecs_service.service
               id:                                      <computed>
               cluster:                                 "default"
               deployment_maximum_percent:              "100"
               deployment_minimum_healthy_percent:      "0"
        """).strip()
        assert expected_plan.replace(" ", "") in output.replace(" ", "")

    def test_correct_number_of_resources(self):
        output = check_output([
            'terraform',
            'plan',
            '-no-color',
            '-target=module.all',
            'test/infra'
        ]).decode('utf-8')

        assert "Plan: 3 to add, 0 to change, 0 to destroy." in output

    def test_no_target_group(self):
        output = check_output([
            'terraform',
            'plan',
            '-no-color',
            '-target=module.no_target_group',
            'test/infra'
        ]).decode('utf-8')

        assert "load_balancer" not in output
