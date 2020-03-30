# tf\_load\_balanced\_ecs\_service

[![Build Status](https://travis-ci.org/mergermarket/tf_load_balanced_ecs_service.svg?branch=master)](https://travis-ci.org/mergermarket/tf_load_balanced_ecs_service)

This module creates an ECS service with resources neccessary to plug into an Application Load Balancer (service role & policy and target group).

## Usage

    module "service" {
        source = "github.com/mergermarket/tf_load_balanced_ecs_service"
        
        cluster     = "default"
        taskdef_arn = "..."
    }

## API

### Parameters

* `name` - (required) Name/name prefix to apply to the resources in the module.
* `vpc_id` - (required) The identifier of the VPC in which to create the target group.
* `task_definition` - (required) The family and revision (family:revision) or full ARN of the task definition that you want to run in your service.
* `cluster` - (default "default") The name of the ECS cluster to deploy the service to. 
* `desired_count` - (default "3") The number of instances of the task definition to place and keep running.
* `container_name` - (default "app") The name of the container to associate with the load balancer (as it appears in a container definition). 
* `container_port` - (default "8000") The port on the container to associate with the load balancer. 
* `deregistration_delay` - (default "10") The amount time for Elastic Load Balancing to wait before changing the state of a deregistering target from draining to unused. The range is 0-3600 seconds.
* `health_check_interval` - (default "5") The approximate amount of time, in seconds, between health checks of an individual target. Minimum value 5 seconds, Maximum value 300 seconds.
* `health_check_path` - (default "/internal/healthcheck") The destination for the health check request. 
* `health_check_timeout` - (default "4") The amount of time, in seconds, during which no response means a failed health check.
* `health_check_healthy_threshold` - (default "2") The number of consecutive health checks successes required before considering an unhealthy target healthy.
* `health_check_unhealthy_threshold` - (default "2") The number of consecutive health check failures required before considering the target unhealthy.
* `health_check_matcher` - (default "200-299") The HTTP codes to use when checking for a successful response from a target. You can specify multiple values (for example, "200,202") or a range of values (for example, "200-299").
* `tags` - (default empty map) Map of tags for the ecs_service.
* `health_check_grace_period_seconds` - Seconds to ignore failing load balancer health checks on newly instantiated tasks to prevent premature shutdown, up to 2147483647. Default 0.

### Outputs

* `target_group_arn` - the ARN of the target group for use by ALB listener rules (e.g. as a parameter to the [tf_alb_listener_rules module](https://github.com/mergermarket/tf_alb_listener_rules)).
