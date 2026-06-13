from __future__ import annotations

import logging
import re

logger = logging.getLogger(__name__)

_BLOCK_FIELDS = {
    "metric_data_queries",
    "metric_dimension",
    "metrics",
}

def correct_block_as_argument(entity: str, hcl: str) -> str:

    for field in _BLOCK_FIELDS:

        pattern = rf"^\s*{field}\s*=\s*.*$"

        def repl(match):

            indent = re.match(
                r"^(\s*)",
                match.group(0)
            ).group(1)

            logger.info(
                "SCHEMA BLOCK FIX %s.%s",
                entity,
                field,
            )

            return (
                f"{indent}{field} {{\n"
                f"{indent}}}"
            )

        hcl = re.sub(
            pattern,
            repl,
            hcl,
            flags=re.MULTILINE,
        )

    return hcl