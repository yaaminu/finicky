import datetime
from unittest.mock import Mock, call

import pytest

from validators import ValidationException, is_int, is_float, is_str, is_date, is_dict, is_list


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

    def test_must_raise_validation_exception_when_input_is_none_but_was_required(self):
        with pytest.raises(ValidationException) as exc:
            is_dict(required=True, schema={})(None)
        assert exc.value.args[0] == f"required but was missing"

    def test_must_return_default_value_when_input_is_none(self):
        address = {"phone": "+233-282123233"}
        assert is_dict(required=False, default=address, schema={})(None) == address

    @pytest.mark.parametrize("input", ["input", ["entry1", "entry2"], 2, 2.3, object()])
    def test_must_raise_validation_error_when_input_is_not_dict(self, input):
        with pytest.raises(ValidationException) as exc_info:
            is_dict(schema={"phone": is_str(required=True)})(input)
        assert exc_info.value.errors == f"expected a dictionary but got {type(input)}"

    @pytest.mark.parametrize(
        ("schema", "input_dict", "expected_errors"),
        [({"phone": is_str(required=True)}, {"phone": None}, {"phone": "required but was missing"}),
         ({"id": is_int(required=True, min=1)}, {"id": -2}, {"id": "'-2' is less than minimum allowed (1)"}),
         ({"user_name": is_str(required=True, max_len=5)}, {"user_name": "yaaminu"},
          {"user_name": "'yaaminu' is longer than maximum required length(5)"})
         ])
    def test_must_validate_input_against_schema(self, schema, input_dict, expected_errors):
        with pytest.raises(ValidationException) as exc:
            is_dict(schema=schema)(input_dict)
        assert expected_errors == exc.value.errors

    def test_must_return_newly_validated_input(self):
        validated_input = is_dict(schema={"phone": is_str(required=True)})({"phone": "+233-23-23283234"})
        assert validated_input == {"phone": "+233-23-23283234"}

    def test_must_clean_validated_input_before_returning(self):
        validated_input = is_dict(schema={"phone": is_str(required=True)})({"phone": " +233-23-23283234"})
        assert validated_input == {"phone": "+233-23-23283234"}


class TestListValidator:
    """
    1. must reject none input whend field is required
    2. must return default value when field isnot required and default is provided
    4. must validate all entries against the validator.
    5. must require all entries to pass validation by default
    6. when all is set to false, must require that at least one entry pass valdiation
    7. must return only validated entries
    6. on error, must return all errors encountered
    """

    def test_must_raise_validation_error_when_input_is_none_but_required_is_true(self):
        with pytest.raises(ValidationException) as exc_info:
            is_list(required=True, validator=is_int())(None)
        assert exc_info.value.errors == "required but was missing"

    def test_must_return_default_value_when_input_is_none(self):
        default = [1, 2]
        assert default == is_list(required=False, default=[1, 2], validator=is_int())(None)

    @pytest.mark.parametrize("input", ["value", {"id": 23}, object, 2.8])
    def test_must_raise_validation_exception_for_non_list_input(self, input):
        with pytest.raises(ValidationException) as exc:
            is_list(validator=Mock())(input)
        assert exc.value.errors == f"expected a list but got {type(input)}"

    def test_must_validate_all_input_against_validator(self):
        validator = Mock()
        is_list(validator=validator)([-1, 8])
        validator.assert_has_calls([call(-1), call(8)])

    @pytest.mark.parametrize(
        ("validator", "input", "errors"),
        [(is_int(min=1), [-1, 2, 8], ["'-1' is less than minimum allowed (1)"]),
         (is_int(max=5), [8, 10],
          ["'8' is greater than maximum allowed (5)", "'10' is greater than maximum allowed (5)"]),
         (is_str(pattern=r"\A\d{3}\Z"), ["2323", "128"], ["'2323' does not match expected pattern(\\A\\d{3}\\Z)"])]
    )
    def test_must_raise_validation_when_at_least_one_entry_is_invalid_by_default(self, validator, input, errors):
        with pytest.raises(ValidationException) as exc:
            is_list(validator=validator)(input)
        assert exc.value.errors == errors

    def test_must_raise_validation_exception_only_when_all_entries_are_invalid_when_all_is_false(self):
        input = [-1, 2, 8]
        try:
            is_list(validator=is_int(min=1), all=False)(input)
        except ValidationException:
            raise AssertionError("should not throw")

    @pytest.mark.parametrize(
        ("validator", "input", "return_val"),
        [(is_int(required=True), [-3, 8, 112], [-3, 8, 112]),
         (is_str(required=True), ["one", "three ", " four "], ["one", "three", "four"]),
         (is_date(format="%Y-%m-%d"), ["2021-02-07 "], [datetime.datetime(year=2021, month=2, day=7)])])
    def test_must_return_newly_validated_input(self, validator, input, return_val):
        assert is_list(validator=validator)(input) == return_val

    def test_must_return_only_valid_inputs_when_all_is_false(self):
        input = [1, -8, 3]
        assert is_list(validator=is_int(min=1), all=False)(input) == [1, 3]
