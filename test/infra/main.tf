provider "aws" {
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_get_ec2_platforms      = true
  skip_region_validation      = true
  skip_requesting_account_id  = true
  max_retries                 = 1
  access_key                  = "a"
  secret_key                  = "a"
  region                      = "eu-west-1"
}

module "target_group" {
  source = "../.."

  name            = "test-service"
  task_definition = "test-taskdef"
  target_group_arn = "arn:aws-partition:service:eu-west-1:aws:resource"
}

module "service" {
  source = "../.."

  name            = "test-service"
  task_definition = "test-taskdef"
  target_group_arn = "arn:aws-partition:service:eu-west-1:aws:resource"
}

module "service_with_long_name" {
  source = "../.."

  name            = "test-service-humptydumptysatonawallhumptydumptyhadagreatfall"
  task_definition = "test-taskdef"
  target_group_arn = "arn:aws-partition:service:eu-west-1:aws:resource"
}

module "role" {
  source = "../.."

  name            = "test-service"
  task_definition = "test-taskdef"
  target_group_arn = "arn:aws-partition:service:eu-west-1:aws:resource"
}

module "policy" {
  source = "../.."

  name            = "test-service"
  task_definition = "test-taskdef"
  target_group_arn = "arn:aws-partition:service:eu-west-1:aws:resource"
}

module "all" {
  source = "../.."

  name            = "test-service"
  task_definition = "test-taskdef"
  target_group_arn = "arn:aws-partition:service:eu-west-1:aws:resource"
}

module "service_with_custom_min_and_max_perecent" {
  source = "../.."

  name                               = "test-service"
  task_definition                    = "test-taskdef"
  target_group_arn                   = "arn:aws-partition:service:eu-west-1:aws:resource"
  deployment_minimum_healthy_percent = "0"
  deployment_maximum_percent         = "100"
}

module "no_target_group" {
  source = "../.."

  name            = "test-service"
  task_definition = "test-taskdef"
}

module "service_with_tags" {
  source = "../.."

  name            = "test-service-with-tags"
  task_definition = "test-taskdef"
  target_group_arn = "arn:aws-partition:service:eu-west-1:aws:resource"

  tags = {
    "name1" = "value1"
    "name2" = "value2"
  }
}

module "service_with_grace_period" {
  source = "../.."

  name            = "test-service"
  task_definition = "test-taskdef"
  target_group_arn = "arn:aws-partition:service:eu-west-1:aws:resource"
  health_check_grace_period_seconds = "15"
}
