from architecture_expander import extract_architecture
from architecture_expander import complete_architecture

queries = [
    "cross account iam role",
    "eks cluster with node group",
    "ecs fargate service behind alb",
    "s3 bucket lifecycle 30 days"
]

for q in queries:

    print("\n" + "=" * 80)
    print("QUERY:", q)

    extracted = extract_architecture(q)

    print("EXTRACTED:")
    print(extracted)

    completed = complete_architecture(extracted)

    print("COMPLETED:")
    print(completed)