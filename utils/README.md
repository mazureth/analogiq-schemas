# Analog Gear Schema Validator

This directory contains utilities for validating gear schema definitions.

## validator.py

A Python-based validator that ensures unit representations conform to the JSON schema.

### Requirements

- Python 3.6 or higher
- jsonschema package: `pip install jsonschema`

### Usage

#### Command Line Usage

Validate a specific unit file:

```bash
python validator.py ../examples/la2a-compressor.json
```

Run tests on all example files:

```bash
python validator.py --test
```

#### Programmatic Usage

```python
from validator import AnalogGearValidator

# Create a validator instance
validator = AnalogGearValidator()

# Validate a unit from file
is_valid, errors = validator.validate_unit_file('path/to/unit.json')

# Validate a unit from data
unit_data = {
    "unitId": "my-unit",
    "name": "My Unit",
    "category": "compressor",
    "faceplateImage": "https://example.com/my-unit.png",
    "width": 800,
    "height": 300,
    "controls": [
        # ... control definitions ...
    ]
}
is_valid, errors = validator.validate_unit(unit_data)

# Format errors for readable output
if not is_valid:
    print(validator.format_errors(errors))
```

## Validation Details

The validator checks:

1. Required properties (unitId, name, category, etc.)
2. Property types and formats
3. Control-specific properties (e.g., min/max for knobs)
4. Enum values (e.g., category must be one of the predefined values)

## Common Validation Errors

- Missing required properties
- Invalid property types
- Invalid enum values for category
- Missing control-specific properties
- Position values outside allowed range (0-1) 