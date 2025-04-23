# Analog Gear Schema Utilities

This directory contains utility scripts for working with the analog gear schema.

## Validator

The `validator.py` script validates unit files against the JSON schema definitions.

### Usage

```bash
# Validate a single unit file
python validator.py ../units/la2a-compressor-1.0.0.json

# Run validation tests
python validator.py --test
```

## Index Generator

The `generate_index.py` script generates an `index.json` file in the `units/` directory containing metadata about all available unit files. This is useful for applications that need to display or filter the available units without loading each individual file.

### Usage

```bash
# Generate index.json in the units directory
python generate_index.py
```

### Output

The script generates a `units/index.json` file with the following structure:

```json
{
  "units": [
    {
      "unitId": "la2a-compressor",
      "name": "LA-2A Compressor",
      "manufacturer": "Teletronix/Universal Audio",
      "tags": ["UA", "Universal Audio", "Teletronix", "optical", "tube", "vintage"],
      "category": "compressor",
      "version": "1.0.0",
      "schemaPath": "units/la2a-compressor-1.0.0.json",
      "thumbnailImage": "https://example.com/images/la2a-thumbnail.png"
    },
    // More units...
  ]
}
```

The generated index includes the following metadata for each unit:
- `unitId`: The unique identifier for the unit
- `name`: The human-readable name of the unit
- `manufacturer`: The company that manufactured the unit
- `tags`: Array of additional searchable tags (optional)
- `category`: The category of the unit (e.g., "compressor", "equalizer")
- `version`: The semantic version of the unit
- `schemaPath`: The relative path to the unit's JSON file
- `thumbnailImage`: The URL to the unit's thumbnail image

### Integration

You can integrate this utility into your build process or CI/CD pipeline to automatically generate an up-to-date index whenever unit files are added or updated.

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

Validate all files in the units directory:

```bash
python validator.py --units
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
    "manufacturer": "My Audio Company",
    "tags": ["custom", "example", "demo"],
    "version": "1.0.0",
    "category": "compressor",
    "faceplateImage": "https://example.com/my-unit.png",
    "thumbnailImage": "https://example.com/my-unit-thumbnail.png",
    "width": 800,
    "height": 300,
    "controls": [
        # ... control definitions ...
    ]
}
is_valid, errors = validator.validate_unit(unit_data)

# Validate all units in the units directory
units_valid, units_results = validator.validate_units_directory()

# Format errors for readable output
if not is_valid:
    print(validator.format_errors(errors))
```

## Validation Details

The validator checks:

1. Required properties (unitId, name, category, version, etc.)
2. Property types and formats
3. Control-specific properties (e.g., min/max for knobs)
4. Enum values (e.g., category must be one of the predefined values)
5. Version consistency in unit files:
   - Filename must match pattern: `unitId-version.json`
   - The unitId in filename must match unitId property in the file
   - The version in filename must match version property in the file
   - Version must follow semantic versioning format

## Common Validation Errors

- Missing required properties
- Invalid property types
- Invalid enum values for category
- Missing control-specific properties
- Position values outside allowed range (0-1)
- Version mismatch between filename and content
- Invalid filename format 