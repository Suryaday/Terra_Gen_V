from generator import build_plan

queries = [
    "jump box ec2 ssh",
    #"cross account iam role",
    #"eks cluster with node group",
    "ecs fargate service behind alb",
    #"s3 bucket lifecycle 30 days"
]

for q in queries:

    print("\n" + "=" * 80)
    print("QUERY:", q)

    plan = build_plan(q)

    print("ROOT:")
    print(plan.root_entities)

    print("ORDERED:")
    print(
        [n.entity for n in plan.ordered_nodes]
    )