from schema_index import find_argument_type
from schema_typing import terraform_type_to_hcl
from generator import infer_variable_type_from_schema

print(
    find_argument_type(
        "aws_ecs_service",
        "subnets",
    )
)

print(
        terraform_type_to_hcl("string"),
        terraform_type_to_hcl("number"),
        terraform_type_to_hcl("bool"),
        terraform_type_to_hcl(["list", "string"]),
        terraform_type_to_hcl(["set", "string"]),
        terraform_type_to_hcl(["map", "string"]),
        terraform_type_to_hcl(["set", ["object", {...}]])
)

print(infer_variable_type_from_schema("aws_lb"))