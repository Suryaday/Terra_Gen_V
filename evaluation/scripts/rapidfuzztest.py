from rapidfuzz import process
from rapidfuzz import fuzz

print(
    process.extractOne(
        "ams_lama_function",
        ["aws_lambda_function"],
        scorer=fuzz.WRatio
    )
)

print(
    process.extractOne(
        "aws_lamda_function",
        ["aws_lambda_function"],
        scorer=fuzz.WRatio
    )
)

print(
    process.extractOne(
        "aws_secuirty_group",
        ["aws_security_group"],
        scorer=fuzz.WRatio
    )
)