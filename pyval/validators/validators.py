from datetime import datetime
import re
from typing import Callable, Union


class ValidationException(Exception):
    def __init__(self, message):
        self.message = message
        super(ValidationException, self).__init__(message)


class ArgumentError(ValueError):
    pass


# noinspection PyShadowingBuiltins
def is_int(required: bool = False, default: int = None, min: int = None, max: int = None
           ) -> Callable[[any], Union[int, None]]:
    """
    Returns a function that when invoked with a given input asserts that the input is a valid integer and that it meets
    a specified criteria.
    :param required: False by default
    :param default: default value to be used when value is `None` (or missing).
    :param min: the minimum allowed value
    :param max: the maximum allowed value
    :return: A callable that when invoked with an input will check that it meets the criteria defined above or raise an
             a validation exception otherwise. It returns the newly validated input on success.
    :raises ArgumentError: when `required` is `True` and default is provided
    """
    if required and default is not None:
        raise ArgumentError("'required' cannot be used together with 'default'")

    def func(value: any) -> Union[int, None]:
        value = value if value is not None else default
        if required and value is None:
            raise ValidationException("required but was missing")
        if not required and value is None:
            return None
        try:
            if isinstance(value, float):
                raise ValueError()
            value = int(value)
            if min is not None and value < min:
                raise ValidationException(f"'{value}' is less than minimum allowed ({min})")
            if max is not None and value > max:
                raise ValidationException(f"'{value}' is greater than maximum allowed ({max})")
            return value
        except ValueError:
            raise ValidationException(f"'{value}' is not a valid integer")

    return func


# noinspection PyShadowingBuiltins
def is_float(required: bool = False, default: float = None, min: float = None, max: float = None, round_to: int = 2
             ) -> Callable[[any], Union[float, None]]:
    """
       Returns a function that when invoked with a given input asserts that the input is a valid floating number
       and that it meets the specified criteria.
       :param required: False by default
       :param default: default value to be used when value is `None` (or missing).
       :param min: the minimum allowed value
       :param max: the maximum allowed value
       :param round_to: the number of decimal places to which the return value must be round to.
       :return: A callable that when invoked with an input will check that it meets the criteria defined above or raise
                an a validation exception otherwise. It returns the newly validated input on success.
       :raises ArgumentError: when `required` is `True` and default is provided
    """
    if required and default is not None:
        raise ArgumentError("'required' cannot be used together with 'default'")

    def func(value: any) -> Union[float, None]:
        value = value if value is not None else default
        if required and value is None:
            raise ValidationException("required but was missing")
        if not required and value is None:
            return None
        try:
            value = round(float(value), round_to)
            if min is not None and value < min:
                raise ValidationException(f"'{value}' is less than minimum allowed ({min})")
            if max is not None and value > max:
                raise ValidationException(f"'{value}' is greater than maximum allowed ({max})")
            return value
        except ValueError:
            raise ValidationException(f"'{value}' is not a valid floating number")

    return func


def is_str(required: bool = False, default: str = None, min_len: int = None, max_len: int = None, pattern: str = None
           ) -> Callable[[any], Union[str, None]]:
    """
       Returns a function that when invoked with a given input asserts that the input is a valid string
       and that it meets the specified criteria. All text are automatically striped off of both trailing and leading
       whitespaces.
       :param required: False by default. When set to True, default value cannot be provided.
       :param default: default value to be used when value is `None` (or missing). Cannot be set together with
                       `required`
       :param min_len: the minimum length allowed. Setting this to 1 effectively rejects empty strings
       :param max_len: the maximum length allowed. Strings longer than this will be rejected
       :param pattern: a valid python regex pattern. Define your patterns carefully with regular expression
                        attacks in mind.
       :return: A callable that when invoked with an input will check that it meets the criteria defined above or raise
                an a validation exception otherwise. It returns the newly validated input on success.
       :raises ArgumentError: when `required` is `True` and default is also provided
    """
    if required and default is not None:
        raise ArgumentError("'required' cannot be used together with 'default'")
    if pattern:
        # compile pattern once and reuse for all validations
        compiled_pattern = re.compile(pattern)

    # noinspection PyShadowingBuiltins
    def func(input: any) -> Union[str, None]:
        input = input or default
        if required and input is None:
            raise ValidationException('required but was missing')
        if not required and input is None:
            return default
        input = str(input).strip()
        if min_len is not None and len(input) < min_len:
            raise ValidationException(f"'{input}' is shorter than minimum required length({min_len})")
        if max_len is not None and len(input) > max_len:
            raise ValidationException(f"'{input}' is longer than maximum required length({max_len})")
        if pattern and compiled_pattern.match(input) is None:
            raise ValidationException(f"'{input}' does not match expected pattern({pattern})")
        return input

    return func


# noinspection PyShadowingBuiltins
def is_date(required: bool = False, default: datetime = None, format: str = "%Y-%m-%d", min: datetime = None,
            max: datetime = None) -> Callable[[Union[datetime, str]], Union[datetime, None]]:
    """
       Returns a function that when invoked with a given input asserts that the input is a valid date
       and that it meets the specified criteria. The function supports both datetime objects and string literals and
       automatically strips off all trailing/leading whitespaces for string literals.

       :param required: False by default. When set to True, default value cannot be provided.
       :param default: default value to be used when value is `None` (or missing). Cannot be set together with
                       `required`
       :param format: The date format, defaults to %Y-%m%-%d. Only used when input date is a string literal.
                      Bear in mind that, python does not support conditional date formatting so all fields specified in
                      the format must be present in the input string.
                      Eg. %Y-%m-%d %H:%M can format 2020-12-12 12:12 and not 2020-12-12 13:12
       :param min: The date after which all input_date should occur, not inclusive
       :param max: The date before which all input date should occur, not inclusive
       :return: A callable that when invoked with an input will check that it meets the criteria defined above or raise
                a validation exception otherwise. It returns the newly validated input on success or the default value
                provided
       :raises ArgumentError: when `required` is `True` and default is also provided
    """
    if required and default:
        raise ArgumentError("Both required and default cannot be provided at the same time")

    def func(input_date: Union[datetime, str]) -> Union[datetime, None]:
        if required and input_date is None:
            raise ValidationException("required but was missing")
        input_date = input_date or default
        if not required and not input_date:
            return None
        if not isinstance(input_date, datetime):
            try:
                input_date = datetime.strptime(str(input_date).strip(), format)
            except ValueError as e:
                raise ValidationException(f"'{input_date}' does not match expected format({format})")
        if min and input_date < min:
            raise ValidationException(
                f"'{input_date.strftime(format)}' occurs before minimum date({min.strftime(format)})")
        if max and input_date > max:
            raise ValidationException(
                f"'{input_date.strftime(format)}' occurs after maximum date({max.strftime(format)})")
        return input_date

    return func


__all__ = ("ArgumentError", "ValidationException", "is_int", "is_float", "is_date", "is_str")
