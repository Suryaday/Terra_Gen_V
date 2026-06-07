from __future__ import annotations

import json
import logging
import re
import os
import httpx
import time


from ollama import (Client, ResponseError)

from tenacity import retry_if_exception_type
from architecture_cache import (get_cached, save_cached)

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential
)

logger = logging.getLogger(__name__)

ARCH_MODEL = os.getenv("ARCH_MODEL", "qwen3:latest")

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

OLLAMA_TIMEOUT = float(os.getenv("OLLAMA_TIMEOUT", "120"))

ARCH_NUM_PREDICT = int(os.getenv("ARCH_NUM_PREDICT","512"))

_ollama_client = Client(host=OLLAMA_HOST, timeout=OLLAMA_TIMEOUT)

ARCHITECTURE_COMPLETIONS = {

    "aws_cloudwatch_event_rule": [
        "aws_cloudwatch_event_target",
        "aws_lambda_permission"
    ],

    "aws_cloudfront_distribution": [
        "aws_s3_bucket",
        "aws_cloudfront_origin_access_identity"
    ],

    "aws_lambda_function": [
        "aws_iam_role",
        "aws_lambda_permission"
    ],

    "aws_lb": [
        "aws_lb_listener", 
        "aws_lb_target_group",
        "aws_security_group"
    ],

    "aws_ecs_service": [
        "aws_appautoscaling_target"
    ],

    "aws_ecs_cluster": [
        "aws_ecs_service"
    ],

    "aws_eks_cluster": [
        "aws_security_group"
    ],

    "aws_appautoscaling_target": [
        "aws_appautoscaling_policy"
    ], 

    "aws_s3_bucket": [
    "aws_s3_bucket_lifecycle_configuration",
    "aws_s3_bucket_versioning"
    ],

    "aws_db_instance": [
    "aws_db_subnet_group"
    ],

    "aws_rds_cluster": [
        "aws_rds_cluster_instance",
        "aws_db_subnet_group",
        "aws_security_group"
    ],

    "aws_apigatewayv2_api": [
        "aws_apigatewayv2_integration",
        "aws_apigatewayv2_stage"
    ],

    "aws_sqs_queue": [
        "aws_sqs_queue_policy",
        "aws_sqs_queue_redrive_policy"
    ],

    "aws_nat_gateway": [
        "aws_route_table",
        "aws_route_table_association"
    ],

    "aws_internet_gateway": [
        "aws_route_table",
        "aws_route_table_association"
    ]
}

SYSTEM_PROMPT = """
/no_think

You are an AWS Terraform Architect.

Return the COMPLETE AWS architecture required
to satisfy the user's request.

Rules:

1. Output ONLY a JSON array.
2. Return Terraform AWS resource types only.
3. Include supporting resources required for the architecture to function.
4. Prefer complete deployable architectures over isolated resources.
5. Do not return explanations.
6. Do not return markdown.

Examples:

Input:
cloudfront distribution with s3 origin

Output:
[
  "aws_cloudfront_distribution",
  "aws_s3_bucket",
  "aws_cloudfront_origin_access_identity"
]

Input:
lambda eventbridge trigger

Output:
[
  "aws_lambda_function",
  "aws_cloudwatch_event_rule",
  "aws_cloudwatch_event_target",
  "aws_lambda_permission"
]
"""


def clean_output( text:str)->str:

    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


@retry(

    stop=stop_after_attempt(3),

    wait=wait_exponential(multiplier=1, min=1, max=8),

    retry=retry_if_exception_type(
        (
            ResponseError,
            ConnectionError,
            TimeoutError,
            httpx.TimeoutException,
            httpx.TransportError
        )
    )

)

def call_llm( query:str)->list[str]:

    start = time.perf_counter()

    try:
        
        logger.info("CALLING OLLAMA FOR ARCHITECTURE EXTRACTION")

        response = _ollama_client.chat(

            model=ARCH_MODEL,

            messages=[

                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },

                {
                    "role": "user",
                    "content": query
                }
            ],

            think=False,

            options={

                "temperature": 0,

                "num_predict": ARCH_NUM_PREDICT
            }
        )

        logger.info("ARCH LLM CALL TOOK %.2fs", time.perf_counter() - start)

    except TypeError:

        logger.warning("Ollama client does not support think=False, retrying without it")

        response = _ollama_client.chat(

            model=ARCH_MODEL,

            messages=[

                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },

                {
                    "role": "user",
                    "content": query
                }
            ],

            options={

                "temperature": 0,

                "num_predict": ARCH_NUM_PREDICT
            }
        )

    text = clean_output(response["message"]["content"])

    match = re.search(r"\[.*\]", text, re.DOTALL)

    if not match:

        return []

    try:

        parsed = json.loads(match.group())

    except Exception:

        return []

    return [x for x in parsed

        if (

            isinstance(x, str)

            and

            x.startswith("aws_")

        )

    ]

def complete_architecture(entities: list[str]) -> list[str]:

    expanded = list(entities)

    seen = set(expanded)

    changed = True

    while changed:
        changed = False
        for entity in list(expanded):

            for completion in ARCHITECTURE_COMPLETIONS.get(entity, []):

                if completion not in seen:

                    expanded.append(completion)

                    seen.add(completion)

                    changed = True

    return expanded

def extract_architecture(query:str)->list[str]:

    cached = get_cached(query)

    if cached is not None:

        logger.info("Architecture cache hit")

        return cached
    
    logger.info("ARCH CACHE MISS")

    logger.info("ARCH QUERY=%s", query)

    logger.info("START ARCH LLM")

    logger.info("ARCH MODEL=%s", ARCH_MODEL)

    logger.info("ARCH TIMEOUT=%s", OLLAMA_TIMEOUT)

    entities = call_llm(query)

    logger.info("END ARCH LLM")

    logger.info("ARCH BEFORE COMPLETION=%s", entities)

    entities = complete_architecture(entities)

    save_cached(query, entities)

    return entities