import re
from typing import Annotated

from pydantic import ValidationError
from pydantic.functional_validators import AfterValidator
from pydantic_core import InitErrorDetails, PydanticCustomError


def check_pwd(pwd: str) -> str:
    """https://github.com/pydantic/pydantic/discussions/7470#discussioncomment-7741826"""
    validation_errors: list[InitErrorDetails] = list()

    if not re.search(r"(?=.*?[A-Z])", pwd):
        validation_errors.append(
            InitErrorDetails(
                type=PydanticCustomError(
                    "value_error",
                    "Is not a valid password",
                    {"reason": "At least one upper case letter"},
                ),
                input=pwd,
                ctx={"error": "At least one upper case letter"},
            )
        )
    if not re.search(r"(?=.*?[a-z])", pwd):
        validation_errors.append(
            InitErrorDetails(
                type=PydanticCustomError(
                    "value_error",
                    "Is not a valid password",
                    {"reason": "At least one lower case letter"},
                ),
                input=pwd,
            )
        )
    if not re.search(r"(?=.*?[0-9])", pwd):
        validation_errors.append(
            InitErrorDetails(
                type=PydanticCustomError(
                    "value_error",
                    "Is not a valid password",
                    {"reason": "At least one digit"},
                ),
                input=pwd,
            )
        )
    if len(pwd) < 8:
        validation_errors.append(
            InitErrorDetails(
                type=PydanticCustomError(
                    "value_error",
                    "Is not a valid password",
                    {"reason": "Minimum eight characters in length"},
                ),
                input=pwd,
            )
        )

    if validation_errors:
        raise ValidationError.from_exception_data(
            "Password invalid",
            line_errors=validation_errors,
        )

    return pwd


CheckPwd = Annotated[str, AfterValidator(check_pwd)]
