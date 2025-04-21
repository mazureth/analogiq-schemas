#!/usr/bin/env python3
"""
Analog Gear Schema Validator

Validates unit representations against the schema definitions
"""

import os
import sys
import json
import argparse
from pathlib import Path

try:
    import jsonschema
    from jsonschema import Draft7Validator, RefResolver
except ImportError:
    print(
        "Error: jsonschema package is required. Install with 'pip install jsonschema'"
    )
    sys.exit(1)


class AnalogGearValidator:
    """Validates analog gear unit representations against JSON schemas"""

    def __init__(self):
        """Initialize the validator with schema paths"""
        # Get the root directory (parent of utils)
        self.root_dir = Path(__file__).parent.parent
        self.schema_dir = self.root_dir / "schemas"

        # Cache for loaded schemas
        self.schema_cache = {}

        # Load the main unit schema
        self.unit_schema = self._load_schema(self.schema_dir / "unit.json")

        # Create a resolver that can handle local references
        self.resolver = RefResolver.from_schema(
            self.unit_schema, handlers={"": self._local_schema_loader}
        )

    def _local_schema_loader(self, uri):
        """
        Load a local schema file for references

        Args:
            uri: The URI to load (e.g. "./controls/knob.json")

        Returns:
            The loaded schema
        """
        # Extract the path from the URI
        if uri.startswith("./"):
            # Get the relative path and join with schema dir
            rel_path = uri
            abs_path = self.schema_dir / rel_path

            return self._load_schema(abs_path)

        raise ValueError(f"Unsupported schema reference: {uri}")

    def _load_schema(self, schema_path):
        """
        Load a schema file

        Args:
            schema_path: Path to the schema file

        Returns:
            The loaded schema as a dict
        """
        if schema_path in self.schema_cache:
            return self.schema_cache[schema_path]

        try:
            with open(schema_path, "r") as f:
                schema = json.load(f)
                self.schema_cache[schema_path] = schema
                return schema
        except Exception as e:
            print(f"Error loading schema {schema_path}: {e}")
            raise

    def validate_unit(self, unit_data):
        """
        Validate a unit against the schema

        Args:
            unit_data: Dict containing the unit data

        Returns:
            Tuple of (is_valid, errors)
        """
        validator = Draft7Validator(self.unit_schema, resolver=self.resolver)
        errors = list(validator.iter_errors(unit_data))
        return len(errors) == 0, errors

    def validate_unit_file(self, file_path):
        """
        Validate a unit from a JSON file

        Args:
            file_path: Path to the unit JSON file

        Returns:
            Tuple of (is_valid, errors)
        """
        try:
            with open(file_path, "r") as f:
                unit_data = json.load(f)
            return self.validate_unit(unit_data)
        except Exception as e:
            return False, [{"message": f"Failed to load or parse file: {e}"}]

    def format_errors(self, errors):
        """
        Format validation errors to be more readable

        Args:
            errors: List of jsonschema validation errors

        Returns:
            Formatted error string
        """
        if not errors:
            return "No validation errors"

        result = []
        for error in errors:
            path = "/".join(str(p) for p in error.path) if error.path else ""
            path = f"/{path}" if path else ""

            message = error.message

            # Add details about the error
            details = ""
            if hasattr(error, "validator_value"):
                if error.validator == "enum":
                    allowed = ", ".join(repr(v) for v in error.validator_value)
                    details = f" (allowed values: {allowed})"
                elif error.validator == "required":
                    details = f" (missing: {', '.join(error.validator_value)})"

            result.append(f"{path}: {message}{details}")

        return "\n".join(result)


def run_tests(validator, examples_dir):
    """
    Run validation tests on all example files

    Args:
        validator: AnalogGearValidator instance
        examples_dir: Directory containing example files
    """
    example_files = [f for f in os.listdir(examples_dir) if f.endswith(".json")]

    if not example_files:
        print("No example files found to validate")
        return True

    print(f"Found {len(example_files)} example files to validate")

    all_valid = True
    for filename in example_files:
        file_path = os.path.join(examples_dir, filename)
        print(f"\nValidating {filename}...")

        valid, errors = validator.validate_unit_file(file_path)

        if valid:
            print(f"✅ {filename} is valid")
        else:
            print(f"❌ {filename} has validation errors:")
            print(validator.format_errors(errors))
            all_valid = False

    print("\nValidation complete.")
    if not all_valid:
        print("❌ Some files failed validation")
    else:
        print("✅ All files are valid")

    return all_valid


def create_and_validate_invalid_example(validator, examples_dir):
    """
    Create and validate an intentionally invalid example

    Args:
        validator: AnalogGearValidator instance
        examples_dir: Directory to save the invalid example
    """
    invalid_path = os.path.join(examples_dir, "_invalid-example.json")

    # Create an invalid example missing required fields
    invalid_example = {
        "unitId": "invalid-unit",
        "name": "Invalid Unit",
        # Missing required category
        "faceplateImage": "https://example.com/images/invalid.png",
        "width": 800,
        # Missing required height
        "controls": [
            {
                "id": "broken-knob",
                "label": "Broken Knob",
                "type": "knob",
                "position": {"x": 0.5, "y": 0.5},
                # Missing required min, max, startAngle, endAngle
                "value": 5,
            }
        ],
    }

    # Write the invalid example to a file
    with open(invalid_path, "w") as f:
        json.dump(invalid_example, f, indent=2)

    print("\nCreated invalid example file for testing")

    # Validate it to demonstrate error detection
    print("\nValidating invalid example...")
    valid, errors = validator.validate_unit_file(invalid_path)

    print("❌ Invalid example validation result (expected to fail):")
    print(validator.format_errors(errors))

    # Clean up
    os.unlink(invalid_path)
    print("Removed invalid example file")


def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(
        description="Validate analog gear unit files against schema"
    )
    parser.add_argument("file", nargs="?", help="Path to unit file to validate")
    parser.add_argument(
        "--test", action="store_true", help="Run tests on example files"
    )

    args = parser.parse_args()

    validator = AnalogGearValidator()

    if args.test:
        examples_dir = os.path.join(validator.root_dir, "examples")
        success = run_tests(validator, examples_dir)
        if success:
            create_and_validate_invalid_example(validator, examples_dir)
        sys.exit(0 if success else 1)

    if not args.file:
        parser.print_help()
        sys.exit(1)

    # Validate a single file
    valid, errors = validator.validate_unit_file(args.file)

    if valid:
        print(f"✅ {args.file} is valid")
        sys.exit(0)
    else:
        print(f"❌ {args.file} has validation errors:")
        print(validator.format_errors(errors))
        sys.exit(1)


if __name__ == "__main__":
    main()
