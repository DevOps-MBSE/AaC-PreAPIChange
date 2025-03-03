import logging

from aac.io.parser import parse
from aac.lang.active_context_lifecycle_manager import get_active_context
from aac.lang.constants import DEFINITION_NAME_SCHEMA, PRIMITIVE_TYPE_STRING, ROOT_KEY_VALIDATION
from aac.lang.definitions.collections import get_definition_by_name, get_definitions_by_root_key
from aac.plugins.contributions.contribution_types import DefinitionValidationContribution
from aac.plugins.validators.root_keys import _get_plugin_definitions, _get_plugin_validations, validate_root_keys

from tests.active_context_test_case import ActiveContextTestCase
from tests.helpers.assertion import assert_definitions_equal, assert_validator_result_failure, assert_validator_result_success
from tests.helpers.parsed_definitions import create_field_entry, create_schema_definition


class TestRootKeysValidator(ActiveContextTestCase):
    def setUp(self) -> None:
        super().setUp()
        logging.disable()  # Hide the error messages generated by these tests from the console.

    def test_module_register_validators(self):
        actual_validator_plugins = _get_plugin_validations()

        validation_definitions = get_definitions_by_root_key(ROOT_KEY_VALIDATION, _get_plugin_definitions())
        self.assertEqual(1, len(validation_definitions))

        validation_definition = validation_definitions[0]
        expected_definition_validation = DefinitionValidationContribution(
            name=validation_definition.name, definition=validation_definition, validation_function=(lambda x: x)
        )
        self.assertEqual(expected_definition_validation.name, actual_validator_plugins[0].name)
        assert_definitions_equal(expected_definition_validation.definition, actual_validator_plugins[0].definition)

    def test_validate_root_keys_valid_key(self):
        test_primitive_reference_field = create_field_entry("ValidPrimitiveField", PRIMITIVE_TYPE_STRING)
        test_definition = create_schema_definition("TestData", fields=[test_primitive_reference_field])

        test_active_context = get_active_context()
        test_active_context.add_definition_to_context(test_definition)

        target_schema_definition = get_definition_by_name(DEFINITION_NAME_SCHEMA, test_active_context.definitions)
        actual_result = validate_root_keys(test_definition, target_schema_definition, test_active_context)

        assert_validator_result_success(actual_result)

    def test_validate_root_keys_invalid_key(self):
        fake_root_key = "not_a_root_key"
        test_definition = create_schema_definition("Test")
        original_root_key = test_definition.get_root_key()
        test_definition.structure[fake_root_key] = test_definition.structure[original_root_key]
        del test_definition.structure[original_root_key]

        # We need to re-parse to make sure lexemes are up-to-date
        test_definition, *_ = parse(test_definition.to_yaml())

        test_active_context = get_active_context()
        test_active_context.add_definition_to_context(test_definition)

        target_schema_definition = test_active_context.get_definition_by_name(original_root_key)
        actual_result = validate_root_keys(test_definition, target_schema_definition, test_active_context)

        assert_validator_result_failure(actual_result, "root", "key", fake_root_key)

    def test_validate_root_keys_valid_extended_root_key(self):
        fake_extended_root_key = "extended_root_key"
        test_definition = create_schema_definition(name="Test", root=fake_extended_root_key)
        test_definition.structure[fake_extended_root_key] = test_definition.structure[test_definition.get_root_key()]
        del test_definition.structure[test_definition.get_root_key()]

        test_active_context = get_active_context()
        test_active_context.add_definitions_to_context([test_definition])

        target_schema_definition = get_definition_by_name(DEFINITION_NAME_SCHEMA, test_active_context.definitions)
        actual_result = validate_root_keys(test_definition, target_schema_definition, test_active_context)

        assert_validator_result_success(actual_result)
