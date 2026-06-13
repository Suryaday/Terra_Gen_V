import schema_index

print(
    schema_index.get_resource_schema(
        "aws_dynamodb_global_secondary_index"
    ) is not None
)

print(
    schema_index.get_resource_schema(
        "aws_dynamodb_table"
    ) is not None
)

schema = schema_index.get_resource_schema(
    "aws_dynamodb_global_secondary_index"
)

print(schema["arguments"].keys())