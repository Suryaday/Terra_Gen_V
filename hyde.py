from __future__ import annotations

import logging
import re

from functools import lru_cache

from ollama import chat
from ollama import ResponseError

from tenacity import retry
from tenacity import wait_exponential
from tenacity import stop_after_attempt
from tenacity import retry_if_exception_type


logger=logging.getLogger(__name__)

OLLAMA_MODEL="qwen3:latest"


SYSTEM_PROMPT="""
Generate hypothetical Terraform provider documentation.

Rules:

1. Mention exact Terraform resource names.

2. Include short example arguments.

3. Include one infrastructure use case.

4. Keep output under 80 words.

5. Prioritize the PRIMARY resource.

6. Mention supporting resources ONLY if directly required.

7. Output documentation-style text.

Do not explain conversationally.
""".strip()


def clean_hyde(text:str)->str:

    text=re.sub(
        r"<think>.*?</think>",
        "",
        text,
        flags=re.DOTALL
    )

    return text.strip()


@lru_cache(maxsize=512)

@retry(

    wait=wait_exponential(
        multiplier=1,
        min=1,
        max=10
    ),

    stop=stop_after_attempt(3),

    retry=retry_if_exception_type((ResponseError, ConnectionError, TimeoutError))

)

def _generate_internal(query:str)->str:

    response=chat(

        model=OLLAMA_MODEL,

        messages=[

            {
                "role":"system",
                "content":SYSTEM_PROMPT
            },

            {
                "role":"user",
                "content":f"""
                Query: {query}

                Generate infrastructure retrieval concepts.
                """
            }

        ]

    )

    output=response["message"]["content"]

    return clean_hyde(output)


def generate_hyde(query:str)->str:

    try:

        output=_generate_internal(query)

        logger.info(
            "HyDE=%s",
            output[:120]
        )

        return output

    except Exception as exc:

        logger.warning(
            "HyDE failed using original query: %s",
            exc
        )

        return query