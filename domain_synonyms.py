from __future__ import annotations

DOMAIN_SYNONYMS={

    "jump box":"bastion aws_instance",

    "bastion host":"aws_instance ssh",

    "ssh server":"aws_instance",

    "alb":"aws_lb",

    "nlb":"aws_lb",

    "elb":"aws_lb",

    "load balancer":"aws_lb",

    "kms":"aws_kms_key",

    "nacl":"aws_network_acl",

    "security group":"aws_security_group",

    "vpc":"aws_vpc",

    "nat gateway":"aws_nat_gateway",

    "ecs":"aws_ecs_cluster",

    "fargate":"aws_ecs_service",

    "route53":"aws_route53_zone",

    "ec2":"aws_instance"

}


def expand_domain_terms(query:str)->str:

    normalized=query.lower()

    for phrase,expansion in DOMAIN_SYNONYMS.items():

        if phrase in normalized:

            normalized=normalized.replace(phrase, f"{phrase} {expansion}")

    return normalized