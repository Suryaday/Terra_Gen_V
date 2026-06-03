from __future__ import annotations

import logging
import string
import re

from typing import Any

from rapidfuzz import fuzz
from rapidfuzz import process


logger=logging.getLogger(__name__)

MIN_SCORE=88


class QueryCorrector:

    def __init__(self, metadata:list[dict[str,Any]]):

        logger.info("Initializing correction vocabulary")

        self._entities=list({

            row["metadata"]["entity"].lower().split("(")[0].strip()

            for row in metadata

            if row["metadata"].get("entity")
        })

        self._services=list({

            row["metadata"]["service"].lower().split("(")[0].strip()

            for row in metadata

            if row["metadata"].get("service")

        })

        logger.info(
            "Loaded vocab entities=%s services=%s",
            len(self._entities),
            len(self._services)
        )

    INFRA_PHRASES={

            "security group":"aws_security_group",

            "lambda function":"aws_lambda_function",

            "ecs service":"aws_ecs_service",

            "iam role":"aws_iam_role",

            "iam policy":"aws_iam_policy",

            "s3 bucket":"aws_s3_bucket",

            "route53 zone":"aws_route53_zone",

            "vpc endpoint":"aws_vpc_endpoint",

            "target group":"aws_lb_target_group",

            "launch template":"aws_launch_template",

            "ecs cluster":"aws_ecs_cluster",

            "eks cluster":"aws_eks_cluster",

            "jump box":"aws_instance aws_security_group bastion",

            "bastion host":"aws_instance aws_security_group",

            "ec2 instance":"aws_instance",

            "eventbridge":"aws_cloudwatch_event_rule",

            "eventbridge trigger":"aws_lambda_permission aws_cloudwatch_event_rule",

            "cloudfront distribution":"aws_cloudfront_distribution",

            "dynamodb table":"aws_dynamodb_table",

            "security groups":"aws_security_group",

            "lambda":"aws_lambda_function",

            "eks":"aws_eks_cluster",

            "transit gateway attachment":"aws_ec2_transit_gateway_vpc_attachment",

            "transit gateway vpc attachment": "aws_ec2_transit_gateway_vpc_attachment",

            "transit gateway":"aws_ec2_transit_gateway",

            "nat gateway":"aws_nat_gateway",

            "internet gateway":"aws_internet_gateway",

            "internet gateway vpc":"aws_internet_gateway",

            "network acl":"aws_network_acl",

            "route table":"aws_route_table",

            "autoscaling group":"aws_autoscaling_group",

            "alb":"aws_lb",

            "nlb":"aws_lb",

            "api gateway":"aws_api_gateway_rest_api",

            "ecs autoscaling": "aws_appautoscaling_target",

            "ecs service autoscaling": "aws_appautoscaling_target aws_ecs_service",

            "waf cloudfront": "aws_wafv2_web_acl aws_cloudfront_distribution",

            "log retention": "aws_cloudwatch_log_group",

            "efs mount": "aws_efs_mount_target aws_efs_file_system",

            "step function": "aws_sfn_state_machine"

    }

    AWS_SHORT_TOKENS = {
        "iam","rds","ecs","eks",
        "s3","ec2","vpc","sns",
        "sqs","kms","alb","nlb",
        "elb","waf","acm",
        "efs", "emr", "ebs",
        "ddb", "asg", "api",
        "fsx", "glue", "mq"
    }

    CORRECTION_STOPWORDS = {

        "architecture",
        "store",
        "security",
        "zone",
        "create",
        "function",
        "resource",
        "manage",
        "update",
        "delete",
        "list",
        "image",
        "get",
        "bucket",
        "cluster",
        "instance",
        "gateway",
        "network",
        "queue",
        "topic",
        "table",
        "stream",
        "volume",
        "snapshot",
        "object",
        "objects",
        "service",
        "endpoint",
        "record",
        "launch",
        "template",
        "policy",
        "role",
        "group",
        "rule",
        "type",
        "name",
        "value",
        "default",
        "configure",
        "attribute",
        "setting",
        "route53",
        "setup",
        "deploy",
        "deployment",
        "provision",
        "host",
        "workflow",
        "website",
        "account",
        "schedule",
        "flow",
        "logs",
        "transit",
        "internet",
        "secret",
        "monitor",
        "access",
        "ssh",
        "user",
        "enable",
        "disable"
    }

    PROTECTED_PHRASES={

        "internet gateway",

        "internet gateway vpc",

        "nat gateway",

        "vpc flow logs",

        "flow logs",

        "private subnet",

        "public subnet",

        "target group",

        "listener rule",

        "route table",

        "network acl",

        "security group",

        "task execution role",

        "execution role",

        "eventbridge cron",

        "eventbridge rule",

        "cloudwatch logs",

        "log retention",

        "cross account",

        "cross account iam role",

        "step function",

        "transit gateway",

        "transit gateway attachment",

        "route53 zone",

        "route53 record",

        "api gateway", 

        "security_group", 

        "public_subnet",

        "private_subnet",

        "jump box", 

        "bastion host"

    }


    def _expand_phrases(self, query:str) -> str:

        expanded = query

        lower = query.lower()

        for phrase,expansion in self.INFRA_PHRASES.items():

            if re.search(rf"\b{re.escape(phrase)}\b", lower):

                logger.info("Expanded '%s' -> '%s'", phrase, expansion)

                expanded += f" {expansion}"

        return expanded

    def _correct_token(self, token:str, candidates:list[str])->str:

        score_cutoff = MIN_SCORE if len(token) >= 8 else 80

        match=process.extractOne(
            token.lower(),
            candidates,
            scorer=fuzz.WRatio,
            score_cutoff=score_cutoff
        )

        if not match: return token

        corrected=match[0]

        if corrected!=token.lower():

            logger.info("Corrected %s -> %s", token,corrected)

        return corrected

    def correct(self, query:str)->str:

        query = self._expand_phrases(query)

        protected=self._protected_words(query)

        corrected=[]

        for word in query.split():

            clean=word.strip(string.punctuation)

            lower=clean.lower()

            if lower in protected:
                corrected.append(word)
                continue

            if lower in self.CORRECTION_STOPWORDS: 
                corrected.append(word)
                continue

            if (len(clean)<4 and lower not in self.AWS_SHORT_TOKENS):

                corrected.append(word)
                continue

            fixed=clean

            if "_" in clean:
                fixed = self._correct_token(clean, self._entities)

            else: 
                fixed = self._correct_token(clean, self._services)

            corrected.append(word.replace(clean,fixed))

        return " ".join(corrected)
    
    def _protected_words(self, query:str)->set[str]:

        lower=query.lower()

        protected=set()

        for phrase in self.PROTECTED_PHRASES:

            if phrase in lower:

                logger.info("Protected phrase detected: '%s'", phrase)

                protected.update(phrase.split())

        return protected