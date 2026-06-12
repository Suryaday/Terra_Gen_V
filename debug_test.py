patterns = [
    "SCHEMA TYPE",
    "HEURISTIC TYPE",
    "VAR TYPE CONFLICT",
    "SCHEMA TYPE CONFLICT",
    "SCHEMA LOOKUP",
    "SCHEMA FINDING",
    "VALIDATOR RETURNED",
    "SCHEMA FIX",
    "SCHEMA: dropped block-as-arg",
]

with open("debug.txt", encoding="utf-16", errors="ignore") as f:
    content = f.read()

for pattern in patterns:
    count = content.count(pattern)
    print(f"{pattern}: {count}")

