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
  target_group_arn = "some-target-group-arn"
}

module "service" {
  source = "../.."

  name            = "test-service"
  task_definition = "test-taskdef"
  target_group_arn = "some-target-group-arn"
}

module "service_with_long_name" {
  source = "../.."

  name            = "test-service-humptydumptysatonawallhumptydumptyhadagreatfall"
  task_definition = "test-taskdef"
  target_group_arn = "some-target-group-arn"
}

module "role" {
  source = "../.."

  name            = "test-service"
  task_definition = "test-taskdef"
  target_group_arn = "some-target-group-arn"
}

module "policy" {
  source = "../.."

  name            = "test-service"
  task_definition = "test-taskdef"
  target_group_arn = "some-target-group-arn"
}

module "all" {
  source = "../.."

  name            = "test-service"
  task_definition = "test-taskdef"
  target_group_arn = "some-target-group-arn"
}

module "service_with_custom_min_and_max_perecent" {
  source = "../.."

  name                               = "test-service"
  task_definition                    = "test-taskdef"
  target_group_arn                   = "some-target-group-arn"
  deployment_minimum_healthy_percent = "0"
  deployment_maximum_percent         = "100"
}

module "no_target_group" {
  source = "../.."

  name            = "test-service"
  task_definition = "test-taskdef"
}
