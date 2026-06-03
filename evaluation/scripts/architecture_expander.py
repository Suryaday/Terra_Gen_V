from __future__ import annotations

import json
import logging
import re

from ollama import chat
from tenacity import retry_if_exception_type
from ollama import ResponseError
from architecture_cache import (get_cached, save_cached)

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential
)

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """
You are an AWS Terraform Architect.

Given a user architecture request, return ONLY JSON.

Rules:

1. Output ONLY terraform AWS resources

2. Return JSON array

3. No explanations

Example:

Input:

lambda eventbridge trigger

Output:

[
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

    retry=retry_if_exception_type((ResponseError, ConnectionError, TimeoutError))

)

def call_llm( query:str)->list[str]:

    response = chat(model="qwen3:latest",

        messages=[

            {

                "role":"system",

                "content":SYSTEM_PROMPT

            },

            {

                "role":"user",

                "content":query

            }

        ],

        options={

            "temperature":0

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


def extract_architecture(query:str)->list[str]:

    cached = get_cached(query)

    if cached is not None:

        logger.info("Architecture cache hit")

        return cached

    entities = call_llm(query)

    save_cached(query, entities)

    return entities