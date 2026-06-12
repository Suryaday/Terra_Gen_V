from schema_index import required_arguments, argument_type

print(
    required_arguments(
        "aws_lb_listener",
        "default_action"
    )
)

print(
    argument_type(
        "aws_lb_listener",
        "default_action",
        "type"
    )
)