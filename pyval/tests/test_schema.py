from unittest.mock import Mock
from pyval.validators import ValidationException
from pyval import validate


class TestSchema:
    def test_validate_must_always_run_all_validations_on_fields(self):
        repo = {"name": "pyval", "version": "1.0.0", "stars": "2000"}
        schema = {"name": Mock(), "version": Mock(), "stars": Mock()}
        validate(schema=schema, data=repo)
        schema.get("name").assert_called_once_with(repo.get("name"))
        schema.get("version").assert_called_once_with(repo.get("version"))
        schema.get("stars").assert_called_once_with(repo.get("stars"))

    def test_must_return_validation_errors(self):
        repo = {"name": "pyval", "version": "1.0.0", "stars": "2000"}
        error_mock = Mock()
        error_mock.side_effect = ValidationException("An error occurred")
        schema = {"name": error_mock, "version": error_mock, "stars": error_mock}
        errors, _ = validate(schema=schema, data=repo)
        assert errors == ["An error occurred", "An error occurred", "An error occurred"]

    def test_validate_must_not_require_hook(self):
        schema = {"name": Mock()}
        hook_mock = Mock()
        validate(schema=schema, data={"name": "pyval"}, hook=None)
        hook_mock.assert_not_called()

    def test_validate_must_run_invoke_hook_on_input_data_when_present(self):
        repo = {"name": "pyval", "version": "1.0.0", "stars": "2000"}
        schema = {"name": Mock(), "version": Mock(), "stars": Mock()}
        hook_mock = Mock()
        validate(schema=schema, data=repo, hook=hook_mock)
        hook_mock.assert_called_once_with(repo)

    def test_validate_must_only_invoke_hook_only_when_field_validations_succeed(self):
        repo = {"name": "pyval", "version": "1.0.0", "stars": "2000"}
        mock_validator = Mock()
        mock_validator.side_effect = ValidationException("an error occured")
        schema = {"name": mock_validator, "version": Mock(), "stars": Mock()}
        hook_mock = Mock()
        validate(schema=schema, data=repo, hook=hook_mock)
        hook_mock.assert_not_called()

    def test_validate_must_include_hook_errors_in_returned_errors(self):
        repo = {"name": "pyval", "version": "1.0.0", "stars": "2000"}
        schema = {"name": Mock(), "version": Mock(), "stars": Mock()}
        hook_mock = Mock()
        hook_mock.side_effect = ValidationException("Hook error")
        errors, _ = validate(schema=schema, data=repo, hook=hook_mock)
        assert "Hook error" in errors

    def test_validate_must_return_what_the_hook_returns(self):
        repo = {"name": "pyval", "version": "1.0.0", "stars": "2000"}
        hook_return_val = {"name": "changed_by hook"}
        schema = {"name": Mock(), "version": Mock(), "stars": Mock()}
        hook = Mock()
        hook.return_value = hook_return_val
        _, validated_repo = validate(schema=schema, data=repo, hook=hook)
        assert validated_repo == hook_return_val

    def test_validate_must_return_newly_validated_data(self):
        repo = {"name": "pyval", "version": "1.0.0", "stars": "2000"}
        hook_return_val = {"name": "changed_by hook"}
        schema = {"name": Mock(), "version": Mock(), "stars": Mock()}
        _, validated_repo = validate(schema=schema, data=repo, hook=None)
        assert validated_repo == repo
