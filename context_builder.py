from __future__ import annotations
import logging
import re

logger = logging.getLogger(__name__)

def u_shape_sort(rows):
    if not rows: 
        return []
    
    ordered = [None] * len(rows)
    left = 0
    right = len(rows) - 1

    for i, row in enumerate(rows):
        if i % 2 == 0:
            # Ranks 1, 3, 5 go to the bottom, filling upwards
            ordered[right] = row
            right -= 1
        else:
            # Ranks 2, 4, 6 go to the top, filling downwards
            ordered[left] = row
            left += 1
            
    return ordered

HEADER_PATTERN = re.compile(

    r"^(?:"
    r"(?:Entity|Service|Section|Title|"
    r"DocumentType|Provider|Category)"
    r":\s*.*?\n"
    r")+",

    re.MULTILINE,
)

def clean_chunk_text(text: str) -> str:

    if not text: return ""

    clean = text.strip()

    clean = re.sub(HEADER_PATTERN, "", clean).strip()

    return clean


def build_xml_context(rows) -> str:

    if not rows:

        return (
            "<context>\n"
            "  No relevant Terraform documentation found.\n"
            "</context>"
        )

    primary = []

    support = []

    examples = []

    for row in rows:

        meta = row.metadata

        section = (meta.get("section", "").lower())

        if (meta.get("_architecture") or meta.get("_dependency")):

            support.append(row)

        elif ("example" in section or "usage" in section):

            examples.append(row)

        else:

            primary.append(row)

    optimal_primary = u_shape_sort(primary)

    context_parts = ["<context>"]

    # ------------------------------------------------------------------
    # SUPPORTING ARCHITECTURE
    # ------------------------------------------------------------------

    if support:

        context_parts.append("  <supporting_architecture>")

        for row in support:

            meta = row.metadata

            tag = ("dependency" if meta.get("_dependency") else "architecture")

            entity = meta.get("entity", "unknown")

            section = meta.get("section", "unknown")

            cross_score = getattr(row,"cross_encoder_score", None)

            rrf_score = getattr(row, "rrf_score", None)

            dense_score = getattr(row, "similarity", None)

            context_parts.append(

                f'    <{tag} '
                f'entity="{entity}" '
                f'section="{section}" '
                f'cross_score="{cross_score}" '
                f'rrf_score="{rrf_score}" '
                f'dense_score="{dense_score}">'
            )

            clean_text = clean_chunk_text(row.text)

            context_parts.append("\n".join(f"      {line}" for line in clean_text.splitlines()))

            context_parts.append(f"    </{tag}>")

        context_parts.append("  </supporting_architecture>")

    # ------------------------------------------------------------------
    # PRIMARY DOCUMENTATION
    # ------------------------------------------------------------------

    if optimal_primary:

        context_parts.append("  <primary_documentation>")

        for row in optimal_primary:

            meta = row.metadata

            entity = meta.get("entity", "unknown")

            section = meta.get("section", "unknown")

            cross_score = getattr(row,"cross_encoder_score", None)

            rrf_score = getattr(row, "rrf_score", None)

            dense_score = getattr(row, "similarity", None)

            context_parts.append(

                f'    <document '
                f'entity="{entity}" '
                f'section="{section}" '
                f'cross_score="{cross_score}" '
                f'rrf_score="{rrf_score}" '
                f'dense_score="{dense_score}">'
            )

            clean_text = clean_chunk_text(row.text)

            context_parts.append("\n".join(f"      {line}" for line in clean_text.splitlines()))

            context_parts.append("    </document>")

        context_parts.append("  </primary_documentation>")

    # ------------------------------------------------------------------
    # EXAMPLES
    # ------------------------------------------------------------------

    if examples:

        context_parts.append("  <terraform_examples>")

        for row in examples:

            meta = row.metadata

            entity = meta.get("entity", "unknown")

            section = meta.get("section", "unknown",)

            context_parts.append(

                f'    <example '
                f'entity="{entity}" '
                f'section="{section}">'
            )

            clean_text = clean_chunk_text(row.text)

            context_parts.append("\n".join(f"      {line}" for line in clean_text.splitlines()))

            context_parts.append("    </example>")

        context_parts.append("  </terraform_examples>")

    context_parts.append("</context>")

    final_context = "\n".join(context_parts)

    logger.info(
        "Built XML context | "
        f"primary={len(primary)} "
        f"support={len(support)} "
        f"examples={len(examples)} "
        f"chars={len(final_context)}"
    )

    return final_context