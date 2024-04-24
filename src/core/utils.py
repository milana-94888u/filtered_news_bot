import re
from pattern.text.en import pluralize


def split_pascal_case_identifier(initial_identifier: str) -> list[str]:
    return re.split(r"(?<=[a-z])(?=[A-Z])", initial_identifier)


def convert_pascal_case_identifier_to_snake_case_plural_identifier(
    initial_identifier: str,
) -> str:
    words = [word.lower() for word in split_pascal_case_identifier(initial_identifier)]
    words[-1] = pluralize(words[-1])
    return "_".join(words)
