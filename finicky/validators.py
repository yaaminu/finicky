from datetime import datetime
import re


class ValidationException(Exception):
    def __init__(self, errors=None):
        self.__errors = errors
        super(ValidationException, self).__init__(errors if type(errors) is str else str(errors))

    @property
    def errors(self):
        return self.__errors


# noinspection PyShadowingBuiltins
def is_int(required=False, default=None, min=None, max=None):
    """
    Returns a function that when invoked with a given input asserts that the input is a valid integer and that it meets
    a specified criteria.
    :param required: False by default
    :param default: default value to be used when value is `None` (or missing).
    :param min: the minimum allowed value
    :param max: the maximum allowed value
    :unittestreturn: A callable that when invoked with an input will check that it meets the criteria defined above or raise an
             a validation exception otherwise. It returns the newly validated input on success.
    :raises ArgumentError: when `required` is `True` and default is provided
    """

    def func(value):
        value = value if value is not None else default
        if required and value is None:
            raise ValidationException("required but was missing")
        if not required and value is None:
            return None
        try:
            if isinstance(value, float):
                raise ValueError()
            value = int(str(value))
            if min is not None and value < min:
                raise ValidationException("'{}' is less than minimum allowed ({})".format(value, min))
            if max is not None and value > max:
                raise ValidationException("'{}' is greater than maximum allowed ({})".format(value, max))
            return value
        except ValueError:
            raise ValidationException("'{}' is not a valid integer".format(value))

    return func


# noinspection PyShadowingBuiltins
def is_float(required=False, default=None, min=None, max=None, round_to=2):
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
    """

    def func(value):
        value = value if value is not None else default
        if required and value is None:
            raise ValidationException("required but was missing")
        if not required and value is None:
            return None
        try:
            value = round(float(str(value)), round_to)
            if min is not None and value < min:
                raise ValidationException("'{}' is less than minimum allowed ({})".format(value, min))
            if max is not None and value > max:
                raise ValidationException("'{}' is greater than maximum allowed ({})".format(value, max))
            return value
        except ValueError:
            raise ValidationException("'{}' is not a valid floating number".format(value))

    return func


def is_str(required=False, default=None, min_len=None, max_len=None, pattern=None):
    """
       Returns a function that when invoked with a given input asserts that the input is a valid string
       and that it meets the specified criteria. All text are automatically striped off of both trailing and leading
       whitespaces.
       :param required: False by default.
       :param default: default value to be used when value is `None` (or missing).
       :param min_len: the minimum length allowed. Setting this to 1 effectively rejects empty strings
       :param max_len: the maximum length allowed. Strings longer than this will be rejected
       :param pattern: a valid python regex pattern. Define your patterns carefully with regular expression
                        attacks in mind.
       :return: A callable that when invoked with an input will check that it meets the criteria defined above or raise
                an a validation exception otherwise. It returns the newly validated input on success.
    """
    if pattern:
        # compile pattern once and reuse for all validations
        compiled_pattern = re.compile(pattern)

    # noinspection PyShadowingBuiltins
    def func(input):
        input = input or default
        if required and input is None:
            raise ValidationException('required but was missing')
        if not required and input is None:
            return default
        input = str(input).strip()
        if min_len is not None and len(input) < min_len:
            raise ValidationException("'{}' is shorter than minimum required length({})".format(input, min_len))
        if max_len is not None and len(input) > max_len:
            raise ValidationException("'{}' is longer than maximum required length({})".format(input, max_len))
        if pattern and compiled_pattern.match(input) is None:
            raise ValidationException("'{}' does not match expected pattern({})".format(input, pattern))
        return input

    return func


# noinspection PyShadowingBuiltins
def is_date(required=False, default=None, format="%Y-%m-%d", min=None,
            max=None):
    """
       Returns a function that when invoked with a given input asserts that the input is a valid date
       and that it meets the specified criteria. The function supports both datetime objects and string literals and
       automatically strips off all trailing/leading whitespaces for string literals.

       :param required: False by default.
       :param default: default value to be used when value is `None` (or missing).
       :param format: The date format, defaults to %Y-%m%-%d. Only used when input date is a string literal.
                      Bear in mind that, python does not support conditional date formatting so all fields specified in
                      the format must be present in the input string.
                      Eg. %Y-%m-%d %H:%M can format 2020-12-12 12:12 and not 2020-12-12 13:12
       :param min: The date after which all input_date should occur, not inclusive
       :param max: The date before which all input date should occur, not inclusive
       :return: A callable that when invoked with an input will check that it meets the criteria defined above or raise
                a validation exception otherwise. It returns the newly validated input on success or the default value
                provided
    """

    def func(input_date):
        if required and input_date is None:
            raise ValidationException("required but was missing")
        input_date = input_date or default
        if not required and not input_date:
            return None
        if not isinstance(input_date, datetime):
            try:
                input_date = datetime.strptime(str(input_date).strip(), format)
            except ValueError as e:
                raise ValidationException("'{}' does not match expected format({})".format(input_date, format))
        if min and input_date < min:
            raise ValidationException(
                "'{}' occurs before minimum date({})".format(input_date.strftime(format), min.strftime(format)))
        if max and input_date > max:
            raise ValidationException(
                "'{}' occurs after maximum date({})".format(input_date.strftime(format), max.strftime(format)))
        return input_date

    return func


def is_dict(schema, required=True, default=None):
    """
    A validator factory that returns a function for validating python dictionaries.

    :param schema: A schema for validating this dictionary, same as the schema described above.
    :param required:`True` when the field is required, `False` otherwise. `True` by default
    :param default: The default value. Only allowed for non-required fields.
    :return: A function that when invoked with a dictionary shall validate it against the criteria specified above

    :raises ArgumentError: When both required and default is set
    """

    def func(_input):
        errors = {}
        _input = _input or default
        if required and _input is None:
            raise ValidationException("required but was missing")
        if type(_input) != dict:
            raise ValidationException("expected a dictionary but got {}".format(type(_input)))
        keys = schema.keys()
        for key in keys:
            try:
                _input[key] = schema[key](_input.get(key))
            except ValidationException as e:
                errors[key] = e.errors
        if errors:
            raise ValidationException(errors)
        return _input

    return func


def is_list(validator, required=True, default=(), min_len=0, max_len=None, all=True):
    """
    A validator factory that returns a function for validating lists. By default, all entries must pass the validation
    else the field would be considered invalid. This can be overridden by setting `all` to `false` (see below).

    :param validator: A validator for validating each entry in the list.
    :param required: `True` when the field is required, `False` otherwise. `True` by default
    :param default:  The default value. Only allowed for non-required fields.
    :param min_len: The minimum number of entries allowed, defaults to 0
    :param max_len: The maximum number of entries, defaults to `None`
    :param all: When `True`, all fields must pass validation for this list to be considered valid. When `False` at
                least one entry must pass validation for this list to be considered valid. Only entries that pass
                validation shall be returned.
    :return: A function that when invoked with a list shall validate it against the criteria specified above

    :raises ArgumentError: When both required and default is set
    """

    def func(_input):
        _input = _input or default
        if required and not _input:
            raise ValidationException("required but was missing")

        if type(_input) is not list:
            raise ValidationException("expected a list but got {}".format(type(_input)))

        errors = []
        validated_input = []
        for index, entry in enumerate(_input, 0):
            try:
                validated_input.append(validator(entry))
            except ValidationException as e:
                errors.append(e.errors)
        if (all and errors) or (not all and len(errors) == len(_input)):
            raise ValidationException(errors)
        return validated_input

    return func


__all__ = ("ValidationException", "is_int", "is_float", "is_date", "is_str", "is_dict", "is_list")
