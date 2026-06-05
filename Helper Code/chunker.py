#Imports

from __future__ import annotations

import json
import logging
import re

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Tuple

import yaml

from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter
)

#Standard Python Logging - prints timestamps and levels

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"

)

logger = logging.getLogger(__name__)

#Paths and Directories

REPO_ROOT = Path("terraform-provider-aws")

DOC_ROOTS = [

    REPO_ROOT / "website" / "docs" / "r",

    REPO_ROOT / "website" / "docs" / "d"

]

OUTPUT_DIR = Path("data") / "chunks"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = (OUTPUT_DIR / "terraform_chunks.json")

#Chunking Parameters
#Some sections like "argument reference" are kept even if short
#Some resources are explicitly marked as primary (not supporting) even if they end with "_attachment"
MIN_CHUNK_CHARS = 60

KEEP_SHORT_SECTIONS = {

    "import",

    "timeouts",

    "argument reference",

    "attributes reference",

    "warning",

    "warnings",

    "deprecated",

    "deprecation"

}


PRIMARY_OVERRIDES = {

    "aws_network_acl_rule",

    "aws_lambda_event_source_mapping"

}


SUPPORTED_SUFFIXES = (

    "_attachment",

    "_association",

    "_grant",

    "_mapping",

    "_configuration"

)

#Langchain Text Splitters
HEADER_SPLITTER = MarkdownHeaderTextSplitter(

    headers_to_split_on=[

        ("#", "h1"),

        ("##", "h2"),

        ("###", "h3"),

        ("####", "h4")

    ],

    strip_headers=False

)


TOKEN_SPLITTER = (

    RecursiveCharacterTextSplitter

    .from_tiktoken_encoder(

        model_name="text-embedding-3-small",

        chunk_size=700,

        chunk_overlap=80,

        separators=[

            "\n### ",

            "\n#### ",

            "\n```",

            "\n* ",

            "\n- ",

            "\n|",

            "\n\n",

            "\n",

            " ",

            ""

        ]

    )

)

#Holds all metadata extracted from frontmatter and file path
#Frozen = True makes instances immutable (good for caching/hashing)
@dataclass(frozen=True)

class SourceDoc:

    path: Path

    doc_type: str

    service: str

    terraform_entity: str

    title: str

    description: str

    layout: str

    subcategory: str

    body: str

#Converts Windows/old Mac line endings to Unix.
def normalize_newlines(text: str) -> str:

    return (

        text

        .replace("\r\n", "\n")

        .replace("\r", "\n")

    )

#Removes the YAML frontmatter block (between ---) and returns the parsed dict plus the remaining body.
def extract_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:

    content = normalize_newlines(content)

    match = re.match(

        r"^---\n(.*?)\n---\n",

        content,

        re.DOTALL

    )

    if not match:

        return {}, content

    try:

        metadata = yaml.safe_load(match.group(1))

        if not isinstance(metadata, dict):

            metadata = {}

    except yaml.YAMLError:

        metadata = {}

    return (metadata, content[match.end():])


def infer_doc_type(

    file_path: Path

) -> str:

    parent = (

        file_path

        .parent

        .name

        .lower()

    )

    if parent == "r":

        return "resource"

    if parent == "d":

        return "data_source"

    return "unknown"


def extract_terraform_entity(

    title: str,

    fallback: str

) -> str:

    title = title.strip()

    if not title:

        return fallback

    parts = title.split(

        ":",

        1

    )

    candidate = (

        parts[-1].strip()

        if len(parts) > 1

        else title

    )

    return (

        candidate

        or fallback

    )


def infer_service(

    subcategory: str

) -> str:

    return (

        subcategory

        .strip()

    )


def classify_resource_kind(

    entity: str | None

) -> str:

    if not entity:

        return "unknown"

    if entity in PRIMARY_OVERRIDES:

        return "primary"

    if entity.endswith(

        SUPPORTED_SUFFIXES

    ):

        return "supporting"

    return "primary"


def resolve_section(

    headers: Dict[str, Any],

    terraform_entity: str

) -> str:

    for level in (

        "h2",

        "h3",

        "h4"

    ):

        value = headers.get(

            level

        )

        if value:

            return str(

                value

            )

    h1 = str(

        headers.get(

            "h1",

            ""

        )

    ).strip()

    normalized_h1 = (h1.replace("Resource:", "").replace("Data Source:", "").strip().lower())

    if (normalized_h1 == terraform_entity.lower()):
        return "overview"
    
    if h1: return h1

    return "overview"


def semantic_header_chunks(

    body: str

):

    docs = HEADER_SPLITTER.split_text(

        body

    )

    docs = [

        d

        for d in docs

        if d.page_content.strip()

    ]

    return TOKEN_SPLITTER.split_documents(

        docs

    )


def load_source_docs():

    failed = 0

    for root in DOC_ROOTS:

        if not root.exists():

            continue

        for file_path in sorted(

            root.rglob(

                "*.markdown"

            )

        ):

            try:

                raw = file_path.read_text(

                    encoding="utf-8"

                )

                metadata, body = (

                    extract_frontmatter(

                        raw

                    )

                )

                yield SourceDoc(

                    path=file_path,

                    doc_type=infer_doc_type(

                        file_path

                    ),

                    service=infer_service(

                        str(

                            metadata.get(

                                "subcategory",

                                ""

                            )

                        )

                    ),

                    terraform_entity=

                    extract_terraform_entity(

                        str(

                            metadata.get(

                                "page_title",

                                ""

                            )

                        ),

                        file_path.stem

                    ),

                    title=str(

                        metadata.get(

                            "page_title",

                            ""

                        )

                    ),

                    description=str(

                        metadata.get(

                            "description",

                            ""

                        )

                    ),

                    layout=str(

                        metadata.get(

                            "layout",

                            ""

                        )

                    ),

                    subcategory=str(

                        metadata.get(

                            "subcategory",

                            ""

                        )

                    ),

                    body=body.strip()

                )

            except Exception:

                failed += 1

                logger.exception(

                    "Failed %s",

                    file_path

                )

    logger.info(

        "Files failed=%d",

        failed

    )


def build_chunks():

    chunks = []

    for source in load_source_docs():

        if not source.body:

            continue

        try:

            split_docs = (

                semantic_header_chunks(

                    source.body

                )

            )

            chunk_counter = 0

            for doc in split_docs:

                raw_text = (

                    doc.page_content

                    .strip()

                )

                headers = dict(

                    getattr(

                        doc,

                        "metadata",

                        {}

                    )

                )

                section = (

                    resolve_section(

                        headers,

                        source.terraform_entity

                    )

                )

                resource_kind = (

                    classify_resource_kind(

                        source.terraform_entity

                    )

                )

                if (

                    len(raw_text)

                    <

                    MIN_CHUNK_CHARS

                    and

                    section.lower()

                    not in

                    KEEP_SHORT_SECTIONS

                ):

                    continue

                enriched = (

                    f"Entity: "

                    f"{source.terraform_entity}\n\n"

                    f"DocumentType: "

                    f"{source.doc_type}\n\n"

                    f"ResourceKind: "

                    f"{resource_kind}\n\n"

                    f"Service: "

                    f"{source.service}\n\n"

                    f"Section: "

                    f"{section}\n\n"

                    f"Title: "

                    f"{source.title}\n\n"

                    f"{raw_text}"

                )

                safe_section = re.sub("_+", "_", re.sub(r"[^a-z0-9]", "_", section.lower())).strip("_")

                chunk = {

                    "chunk_id": (

                        f"{source.doc_type}_"

                        f"{source.terraform_entity}_"

                        f"{safe_section}_"

                        f"{chunk_counter:03}"

                    ),

                    "source_file":

                    source.path.name,

                    "source_path":

                    str(source.path),

                    "doc_type":

                    source.doc_type,

                    "service":

                    source.service,

                    "terraform_entity":

                    source.terraform_entity,

                    "title":

                    source.title,

                    "subcategory":

                    source.subcategory,

                    "description":

                    source.description,

                    "layout":

                    source.layout,

                    "chunk_index":

                    chunk_counter,

                    "header_metadata":

                    headers,

                    "section":

                    section.lower(),

                    "resource_kind":

                    resource_kind,

                    "text":

                    enriched,

                    "char_count":

                    len(enriched)

                }

                chunks.append(

                    chunk

                )

                chunk_counter += 1

        except Exception:

            logger.exception(

                "Chunk failed %s",

                source.path

            )

    return chunks


def main():

    logger.info(

        "Building chunks..."

    )

    chunks = build_chunks()

    with OUTPUT_FILE.open(

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            chunks,

            f,

            indent=2,

            ensure_ascii=False

        )

    logger.info(

        "Chunks=%d",

        len(chunks)

    )

    logger.info(

        "Saved=%s",

        OUTPUT_FILE

    )


if __name__ == "__main__":

    main()