from typing import Callable, Tuple

from pyval.validators import ValidationException


def validate(schema: dict, data: dict, hook: Callable[[dict], dict] = None) -> Tuple[dict, dict]:
    """
    Given an input named `data` validate it against `schema` returning errors encountered if any and the input data.
    It's important to note that, validation continues even if an error is encountered.
    :param schema: The schema against which the input should be validated. A schema is essentially a mapping of field
    names and their corresponding validators. The keys must match exactly to fields in the input data.
    Pyval comes with a set of standard validators defined in `pyval.validators` but you can write your own
    if your need a more customized one.

    A validator is a function which takes in a single argument and returns the validated
    data on success. On failure, it must raise a `pyval.validators.ValidationException`. To illustrate in code:
    ```
        def my_custom_batch_no_validator(input):
            if not input:
                raise ValidationException("This field is required")
            elif not input.contains("prefix_")
                raise ValidationException("This field must start with `prefix_`")
            else:
                # you can modify the value, like striping off whitespace, rounding up the number etc
                return input.strip()
    ```
    :param data: The input data to be validated, cannot be none
    :param hook: An optional custom hook function that shall be invoked  when all fields have passed validation. It is
                 especially useful in situations where the validity of the input also conditionally relies on multiple
                 fields. it takes as an input, the newly validated data and must return the input on success
                 or raise a `pyval.validators.ValidationException` on failure. This hook may modify the input before
                 returning it.
    :return: A tuple of the form (errors:str[], validated_data)
    """
    errors = {}
    for key in schema:
        try:
            schema[key](data.get(key))
        except ValidationException as e:
            errors[key] = e.errors
    if hook and not errors:
        try:
            data = hook(data)
        except ValidationException as e:
            errors["___hook"] = e.errors
    return errors, data
