import re
import unittest
import os
import time
from textwrap import dedent
from subprocess import check_call, check_output

cwd = os.getcwd()

class TestCreateTaskdef(unittest.TestCase):

    def setUp(self):
        check_call([ 'terraform', 'get', 'test/infra' ])

    
    def test_create_taskdef(self):
        # ms since epoch
        name = 'test-' + str(int(time.time() * 1000))

        output = check_output([
            'terraform',
            'plan',
            '-var', 'name={}'.format(name),
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        assert dedent("""
            + module.service.aws_alb_target_group.target_group
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
        """).strip() in output, output

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

        assert dedent("""
            + module.service.aws_iam_role.role
                arn:                "<computed>"
                assume_role_policy: "{\\n  \\"Version\\": \\"2012-10-17\\",\\n  \\"Statement\\": [\\n    {\\n      \\"Action\\": \\"sts:AssumeRole\\",\\n      \\"Principal\\": { \\"Service\\": \\"ecs.amazonaws.com\\" },\\n      \\"Effect\\": \\"Allow\\"\\n    }\\n  ]\\n}\\n"
                create_date:        "<computed>"
                name:               "<computed>"
                name_prefix:        "test-service-service-role"
                path:               "/"
                unique_id:          "<computed>"
        """).strip() in output

        assert dedent("""
            + module.service.aws_iam_role_policy.policy
                name:        "<computed>"
                name_prefix: "test-service-service-policy"
                policy:      "{\\n  \\"Version\\": \\"2012-10-17\\",\\n  \\"Statement\\": [\\n    {\\n      \\"Effect\\": \\"Allow\\",\\n      \\"Action\\": [\\n        \\"ec2:AuthorizeSecurityGroupIngress\\",\\n        \\"ec2:Describe*\\",\\n        \\"elasticloadbalancing:DeregisterInstancesFromLoadBalancer\\",\\n        \\"elasticloadbalancing:DeregisterTargets\\",\\n        \\"elasticloadbalancing:Describe*\\",\\n        \\"elasticloadbalancing:RegisterInstancesWithLoadBalancer\\",\\n        \\"elasticloadbalancing:RegisterTargets\\"\\n      ],\\n      \\"Resource\\": \\"*\\"\\n    }\\n  ]\\n}\\n"
                role:        "${aws_iam_role.role.id}"
        """).strip() in output

        assert dedent("""
            Plan: 4 to add, 0 to change, 0 to destroy.
        """).strip() in output
