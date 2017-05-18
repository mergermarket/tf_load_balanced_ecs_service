resource "aws_iam_role" "role" {
  name_prefix        = "${var.name}-service-role"

  # from http://docs.aws.amazon.com/AmazonECS/latest/developerguide/service_IAM_role.html
  assume_role_policy = <<END
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
END
}


resource "aws_iam_role_policy" "policy" {
  role        = "${aws_iam_role.role.id}"
  name_prefix = "${var.name}-service-policy"

  # from http://docs.aws.amazon.com/AmazonECS/latest/developerguide/service_IAM_role.html (step 7)
  policy      = <<END
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
END
}
