from __future__ import annotations
import string
from enum import Enum
import re


class QueryIntent(str,Enum):

    ARGUMENTS="arguments"

    EXAMPLE="example"

    ARCHITECTURE="architecture"

    RESOURCE="resource"

    DEPENDENCY="dependency"


ARGUMENT_WORDS = {"argument", "arguments", "parameter", "parameters", "attribute", "attributes", "setting", "settings", "timeout", "limit"}
EXAMPLE_WORDS = {"example", "sample", "usage", "snippet", "code", "template"}
ARCHITECTURE_WORDS = {"architecture", "design", "diagram", "topology", "pattern"}
ARCHITECTURE_TERMS={"trigger", "invoke", "connect", "pipeline", "workflow", "eventbridge", "notification", "stream", "queue", "fanout", "fan-out", "target"}
DEPENDENCY_WORDS = {"dependency", "dependencies", "integrate", "integration", "relationship", "attach"}



def classify(query:str)->QueryIntent:

    clean_query=re.sub(rf"[{re.escape(string.punctuation)}]", " ", query).lower()
    tokens = set(clean_query.split())

    if tokens & ARGUMENT_WORDS:
        return QueryIntent.ARGUMENTS
    if tokens & EXAMPLE_WORDS:
        return QueryIntent.EXAMPLE
    if (tokens & (ARCHITECTURE_WORDS | ARCHITECTURE_TERMS)):
        return QueryIntent.ARCHITECTURE
    if tokens & DEPENDENCY_WORDS:
        return QueryIntent.DEPENDENCY

    return QueryIntent.RESOURCE