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
  vpc_id          = "test-vpc"
  task_definition = "test-taskdef"
}

module "service" {
  source = "../.."

  name            = "test-service"
  vpc_id          = "test-vpc"
  task_definition = "test-taskdef"
}

module "service_with_long_name" {
  source = "../.."

  name            = "test-service-humptydumptysatonawallhumptydumptyhadagreatfall"
  vpc_id          = "test-vpc"
  task_definition = "test-taskdef"
}

module "service_with_tags" {
  source = "../.."

  name            = "test-service-with-tags"
  vpc_id          = "test-vpc"
  task_definition = "test-taskdef"

  tags = {
    "name1" = "value1"
    "name2" = "value2"
  }
}

module "role" {
  source = "../.."

  name            = "test-service"
  vpc_id          = "test-vpc"
  task_definition = "test-taskdef"
}

module "policy" {
  source = "../.."

  name            = "test-service"
  vpc_id          = "test-vpc"
  task_definition = "test-taskdef"
}

module "all" {
  source = "../.."

  name            = "test-service"
  vpc_id          = "test-vpc"
  task_definition = "test-taskdef"
}

output "target_group_arn" {
  value = "${module.service.target_group_arn}"
}
