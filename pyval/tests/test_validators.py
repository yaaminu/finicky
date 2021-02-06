import datetime

import pytest

from pyval.validators import ValidationException, is_int, ArgumentError, is_float, is_str, is_date


# noinspection PyShadowingBuiltins
class TestIntValidator:

    def test_must_raise_validation_exception_when_input_is_none_and_required_is_true(self):
        with pytest.raises(ValidationException) as exc_info:
            is_int(required=True)(None)
        assert exc_info.value.args[0] == "required but was missing"

    @pytest.mark.parametrize("input", ["3a", "", "3.5", 3.5, "20/12/2020"])
    def test_must_raise_validation_exception_when_input_is_not_a_valid_int(self, input):
        with pytest.raises(ValidationException) as exc_info:
            is_int()(input)
        assert exc_info.value.args[0] == f"'{input}' is not a valid integer"

    @pytest.mark.parametrize("input,min", [(-1, 0), (0, 1), (8, 9), (11, 120)])
    def test_must_raise_validation_exception_when_input_is_less_than_minimum_allowed(self, input, min):
        with pytest.raises(ValidationException) as exc_info:
            is_int(min=min)(input)
        assert exc_info.value.args[0] == f"'{input}' is less than minimum allowed ({min})"

    @pytest.mark.parametrize("input,max", [(1, 0), (0, -1), (10, 9), (100, 99)])
    def test_must_raise_validation_exception_when_input_is_greater_than_maximum_allowed(self, input, max):
        with pytest.raises(ValidationException) as exc_info:
            is_int(max=max)(input)
        assert exc_info.value.args[0] == f"'{input}' is greater than maximum allowed ({max})"

    def test_must_raise_error_when_input_is_required_and_default_is_set(self):
        with pytest.raises(ArgumentError):
            is_int(required=True, default=1)(8)

    @pytest.mark.parametrize("input, min, max", [(8, 2, 10), (0, -1, 1), ("8", 1, 12)])
    def test_must_return_input_upon_validation(self, input, min, max):
        assert is_int(min=min, max=max)(input) == int(input)

    def test_must_return_default_provided_when_input_is_missing(self):
        assert is_int(default=8)(None) == 8

    def test_must_return_none_when_input_is_none_and_required_is_false(self):
        assert is_int(required=False)(None) is None


# noinspection PyShadowingBuiltins
class TestFloatValidator:

    def test_must_raise_validation_exception_when_input_is_none_and_required_is_true(self):
        with pytest.raises(ValidationException) as exc_info:
            is_float(required=True)(None)
        assert exc_info.value.args[0] == "required but was missing"

    @pytest.mark.parametrize("input", ["3a", "", "20/12/2020"])
    def test_must_raise_validation_exception_when_input_is_not_a_valid_int(self, input):
        with pytest.raises(ValidationException) as exc_info:
            is_float()(input)
        assert exc_info.value.args[0] == f"'{input}' is not a valid floating number"

    @pytest.mark.parametrize("input,min", [(-0.99, 0), (0.1, 0.12), (8.9, 9), (13, 120)])
    def test_must_raise_validation_exception_when_input_is_less_than_minimum_allowed(self, input, min):
        with pytest.raises(ValidationException) as exc_info:
            is_float(min=min)(input)
        assert exc_info.value.args[0] == f"'{float(input)}' is less than minimum allowed ({min})"

    @pytest.mark.parametrize("input,max", [(0.2, 0), (-0.1, -0.2), (9.9, 9), (99.1, 99)])
    def test_must_raise_validation_exception_when_input_is_greater_than_maximum_allowed(self, input, max):
        print(input, max)
        with pytest.raises(ValidationException) as exc_info:
            is_float(max=max)(input)
        assert exc_info.value.args[0] == f"'{float(input)}' is greater than maximum allowed ({max})"

    def test_must_raise_error_when_input_is_required_and_default_is_set(self):
        with pytest.raises(ArgumentError):
            is_float(required=True, default=1)(0.7)

    @pytest.mark.parametrize("input, min, max", [(8.2, 0.1, 8.3), (0.1, -0.1, 0.2), ("0.2", 0.1, 12)])
    def test_must_return_input_upon_validation(self, input, min, max):
        assert is_float(min=min, max=max)(input) == float(input)

    def test_must_return_default_provided_when_input_is_missing(self):
        assert is_float(default=0.5)(None) == 0.5

    @pytest.mark.parametrize("input, expected", [(8.589, 8.59), (0.182, 0.18), ("-0.799", -0.80)])
    def test_must_round_returned_value_to_2_decimal_places_by_default(self, input, expected):
        assert is_float()(input) == expected

    @pytest.mark.parametrize("input, expected, round_to",
                             [(8.589, 9, 0), ("-0.799", -0.8, 1), (0.3333, 0.33, 2), (0.182, 0.182, 3), ])
    def test_must_round_returned_value_to_provided_decimal_places(self, input, expected, round_to):
        assert is_float(round_to=round_to)(input) == expected

    def test_must_return_none_when_input_is_none_and_required_is_false(self):
        assert is_float(required=False)(None) is None


# noinspection PyShadowingBuiltins
class TestStrValidator:

    def test_must_raise_argument_error_when_both_required_and_default_are_provided(self):
        with pytest.raises(ArgumentError):
            is_str(required=True, default="default value")("GH-A3323")

    def test_must_raise_exception_when_input_is_none_and_required_is_true(self):
        with pytest.raises(ValidationException) as exc_info:
            is_str(required=True)(None)
        assert exc_info.value.args[0] == 'required but was missing'

    @pytest.mark.parametrize("input, expected",
                             [("  GH-A323 ", "GH-A323"), ("GH-A3 ", "GH-A3"), (33, "33"), ("GH-A3", "GH-A3")])
    def test_must_automatically_strip_trailing_or_leading_whitespaces_on_inputs(self, input, expected):
        assert is_str()(input) == expected

    @pytest.mark.parametrize("input,min_len", [("GH ", 3), (" G ", 2), ("Python", 7), ("  ", 1)])
    def test_must_raise_validation_exception_when_input_is_shorter_than_minimum_required_length(self, input, min_len):
        with pytest.raises(ValidationException) as exc_info:
            is_str(min_len=min_len)(input)
        assert exc_info.value.args[0] == f"'{input.strip()}' is shorter than minimum required length({min_len})"

    @pytest.mark.parametrize("input,max_len", [("GHAN ", 3), (" GH ", 1), ("Python GH", 7)])
    def test_must_raise_validation_exception_when_input_is_shorter_than_minimum_required_length(self, input, max_len):
        with pytest.raises(ValidationException) as exc_info:
            is_str(max_len=max_len)(input)
        assert exc_info.value.args[0] == f"'{input.strip()}' is longer than maximum required length({max_len})"

    @pytest.mark.parametrize("input, pattern", [("GH", r"\bGHA$"), ("GH-1A", r"\bGH-\d?$")])
    def test_must_raise_validation_error_when_input_does_not_match_expected_pattern(self, input, pattern):
        with pytest.raises(ValidationException) as exc_info:
            is_str(pattern=pattern)(input)
        assert exc_info.value.args[0] == f"'{input}' does not match expected pattern({pattern})"

    def test_must_return_default_when_input_is_none(self):
        assert is_str(default="Text")(None) == "Text"

    def test_must_return_none_when_input_is_none_and_required_is_false_and_default(self):
        assert is_str(required=False)(None) is None


# noinspection PyShadowingBuiltins
class TestIsDateValidator:

    def test_must_raise_validation_exception_when_input_is_missing_and_required_is_true(self):
        with pytest.raises(ValidationException) as exc_info:
            is_date(required=True)(None)
        assert exc_info.value.args[0] == "required but was missing"

    def test_must_raise_argument_error_when_required_is_true_and_default_is_provided(self):
        with pytest.raises(ArgumentError):
            is_date(required=True, default=datetime.datetime.now())(None)

    @pytest.mark.parametrize("format,input",
                             [("%d-%m-%Y", "20/12/2020"), ("%d-%m-%Y", "38-01-2020"), ("%d/%m/%Y", "31/06/2020")])
    def test_must_raise_validation_exception_when_input_str_does_not_match_format(self, format, input):
        with pytest.raises(ValidationException) as exc_info:
            is_date(format=format)(input)
        assert exc_info.value.args[0] == f"'{input}' does not match expected format({format})"

    @pytest.mark.parametrize("input", ["2020-12-20", "2021-01-31 ", " 1999-08-12 "])
    def test_must_use_iso_8601_format_when_format_is_not_supplied(self, input):
        date = is_date()(input)
        assert date == datetime.datetime.strptime(input.strip(), "%Y-%m-%d")

    @pytest.mark.parametrize("input,min", [("2020-12-19", "2020-12-20"), ("2020-12-31", "2021-01-31")])
    def test_must_raise_validation_exception_when_date_is_older_than_latest_by_if_defined(self, input, min):
        with pytest.raises(ValidationException) as exc_info:
            is_date(min=datetime.datetime.strptime(min, "%Y-%m-%d"))(input)
        assert exc_info.value.args[0] == f"'{input}' occurs before minimum date({min})"

    @pytest.mark.parametrize("max,input", [("2020-12-19", "2020-12-20"), ("2020-12-31", "2021-01-31",)])
    def test_must_raise_validation_exception_when_date_is_older_than_latest_by_if_defined(self, max, input):
        with pytest.raises(ValidationException) as exc_info:
            is_date(max=datetime.datetime.strptime(max, "%Y-%m-%d"))(input)
        assert exc_info.value.args[0] == f"'{input}' occurs after maximum date({max})"

    def test_must_support_datetime_objects_as_input_dates(self):
        today = datetime.datetime.today()
        assert today == is_date()(today)

    def test_when_input_date_is_none_must_return_default_date_if_available(self):
        today = datetime.datetime.today()
        assert today == is_date(default=today)(None)

    def test_must_return_none_when_input_is_none_and_required_is_false_and_default_is_not_provided(self):
        assert is_date(required=False)(None) is None

    @pytest.mark.parametrize("input", ["2020-12-20", "2021-01-31", "1999-08-12"])
    def test_must_return_newly_validated_date_as_datetime_object(self, input):
        assert is_date()(input) == datetime.datetime.strptime(input, "%Y-%m-%d")


class TestDictValidator:
    """
    1. must reject None input when field is required
    2. must return default value when field is not required and default provided
    3. must raise argument error when required is true and default value is provided
    4. must validate input against schema
    5. must not require schema
    """
    pass


class TestListValidator:
    """
    1. must reject none input whend field is required
    2. must return default value when field isnot required and default is provided
    3. must raise invaldi argument error when field is required and default is not none
    4. must validate all entries against the validator.
    5. must require all entries to pass validation by default
    6. when all is set to false, must require that at least one entry pass valdiation
    7. must return only validated entries
    6. on error, must return all errors encountered
    """
    pass
