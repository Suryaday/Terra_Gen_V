from __future__ import annotations

from auto_dependency_map import RESOURCE_DEPENDENCIES


MAX_DEPTH = 1


def expand_entities(
    entities:list[str],
    depth:int=MAX_DEPTH,
    hard_only:bool=True
)->list[str]:

    seen=set()

    expanded=[]

    current=entities[:]

    for _ in range(depth+1):

        next_level=[]

        for entity in current:

            if (
                not entity
                or entity in seen
            ):
                continue

            seen.add(entity)

            expanded.append(entity)

            deps=RESOURCE_DEPENDENCIES.get(
                entity,
                {}
            )

            next_level.extend(
                deps.get(
                    "hard",
                    []
                )
            )

            if not hard_only:

                next_level.extend(

                    deps.get(
                        "optional",
                        []
                    )

                )

        current=next_level

    return expanded