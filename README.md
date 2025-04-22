# Analog Gear Serialization Schema

This repository contains JSON schema definitions for simulating analog audio equipment. The schema standardizes how analog gear controls (knobs, switches, faders, etc.) are digitally represented and manipulated in DAW plugins or gear recall tools.

## Schema Structure

The schema is organized as follows:

- `schemas/`: Contains the JSON schema definitions
  - `controls/`: Individual control type schemas
    - `knob.json`: Schema for rotary knobs
    - `switch.json`: Schema for multi-position switches
    - `button.json`: Schema for buttons (on/off)
    - `fader.json`: Schema for linear faders
  - `unit.json`: Main schema that brings all controls together
- `units/`: Contains actual unit implementations
  - `index.json`: Contains metadata about all available units
- `utils/`: Contains utility scripts
  - `validator.py`: Validates unit files against the schema
  - `generate_index.py`: Generates the units/index.json file

## Control Types

### Knob

Represents a rotary control with a defined angle range and min/max values:

```json
{
  "type": "knob",
  "min": 0,
  "max": 10,
  "step": 0.1,
  "startAngle": 30,
  "endAngle": 330,
  "value": 5,
  "zIndex": 1,
  "image": "https://example.com/images/black-knob.png"
}
```

### Switch

Represents a multi-position switch with named options:

```json
{
  "type": "switch",
  "options": ["Option 1", "Option 2", "Option 3"],
  "currentIndex": 1,
  "image": "https://example.com/images/toggle-switch.png"
}
```

### Button

Represents a button that can be momentary or latching:

```json
{
  "type": "button",
  "momentary": false,
  "state": true,
  "image": "https://example.com/images/push-button.png"
}
```

### Fader

Represents a linear control with horizontal or vertical orientation:

```json
{
  "type": "fader",
  "min": -12,
  "max": 12,
  "value": 0,
  "orientation": "vertical",
  "image": "https://example.com/images/slider.png"
}
```

## Visual Representation

Each control includes an optional `image` property that specifies a URI to the image representing that specific control's visual appearance. This allows for accurate visual representation of different control types across various gear models, as the appearance of knobs, switches, and other controls often varies between different units.

When building a UI with these schemas:
1. Use the unit's `faceplateImage` as the background for the full view
2. Use the unit's `thumbnailImage` for smaller representations in plugin interfaces
3. Position each control at its specified coordinates
4. Use each control's `image` property to render the specific visual appearance of that control

## Unit Schema

The `unit.json` schema defines a complete piece of analog gear, including its ID, name, category, version, faceplate image, thumbnail image, dimensions, and an array of controls with their positions.

```json
{
  "unitId": "example-unit",
  "name": "Example Unit",
  "version": "1.0.0",
  "category": "compressor",
  "faceplateImage": "https://example.com/images/faceplate.png",
  "thumbnailImage": "https://example.com/images/thumbnail.png",
  "width": 800,
  "height": 300,
  "controls": [
    // Control definitions
  ]
}
```

### Versioning

Units follow semantic versioning (SemVer) for tracking changes:

- **MAJOR** version for incompatible changes
- **MINOR** version for new backwards-compatible features
- **PATCH** version for backwards-compatible bug fixes

The version is included both in the filename (`unitId-version.json`) and as a property in the JSON itself.

### Categories

Units must be categorized using one of the predefined categories in the `category` property. This ensures consistency and prevents fragmentation (e.g., having both "compressor" and "comp" as separate categories).

The allowed categories are:

- `compressor` - Dynamic range compressors
- `equalizer` - Graphic, parametric, and other EQs
- `preamp` - Microphone and instrument preamps
- `channel-strip` - Combined preamp, EQ, and dynamics processors
- `mixer` - Mixing consoles and summing amplifiers
- `reverb` - Reverb and echo chambers
- `delay` - Delay and echo units
- `limiter` - Peak limiters and brickwall limiters
- `gate` - Noise gates and expanders
- `de-esser` - Sibilance controllers
- `multi-effects` - Units with multiple effect types

Using a fixed set of categories makes it easier to organize, search, and filter gear in applications that use this schema.

### Dimensions and Layout

The unit schema includes two important properties for defining the drawable space:

- `width`: The width of the drawable space in pixels
- `height`: The height of the drawable space in pixels

These dimensions provide context for the relative positions of controls. Each control's position (`x` and `y` values between 0 and 1) can be converted to absolute coordinates by multiplying by the unit's width and height.

For example, if a unit has a width of 800px and a control has an x position of 0.25, the absolute x coordinate would be 200px (0.25 * 800).

## Units Directory

The `units/` directory contains actual implementations of gear units following this schema. Each unit is versioned according to semantic versioning rules, with the version number included in both the filename and the JSON content.

For example:
- `units/la2a-compressor-1.0.0.json`
- `units/api-560-eq-1.0.0.json`

See the [units README](units/README.md) for more information about available units and versioning guidelines.

## Units Index

The repository includes an `index.json` file in the `units/` directory which contains metadata about all available units. This index is automatically generated using the `utils/generate_index.py` script.

The index file makes it easy for applications to:
- Display a list of all available units
- Show thumbnails and names without loading the full unit files
- Filter units by category
- Access unit files directly via the schema path

Sample index.json structure:
```json
{
  "units": [
    {
      "unitId": "la2a-compressor",
      "name": "LA-2A Compressor",
      "category": "compressor",
      "version": "1.0.0",
      "schemaPath": "units/la2a-compressor-1.0.0.json",
      "thumbnailImage": "https://example.com/images/la2a-thumbnail.png"
    },
    {
      "unitId": "api-560-eq",
      "name": "API 560 10-Band Graphic Equalizer",
      "category": "equalizer",
      "version": "1.0.0",
      "schemaPath": "units/api-560-eq-1.0.0.json",
      "thumbnailImage": "https://example.com/images/api-560-thumbnail.png"
    }
  ]
}
```

To regenerate the index file after adding or updating units, run:
```bash
python utils/generate_index.py
```

## Examples

The `examples/` directory contains sample implementations that demonstrate how to use the schema.

## Schema Validation

This repository includes a Python-based validator utility to ensure that unit representations meet the schema requirements.

### Requirements

- Python 3.6+
- **Required**: jsonschema package

You can install the dependencies using pip:
```bash
pip install -r requirements.txt
```

> **Note**: The validator will not work without the jsonschema package installed.

### Validating Unit Files

You can validate a unit file against the schema using the provided command-line utility:

```bash
python utils/validator.py examples/la2a-compressor.json
```

The validator will check if the file conforms to the schema and display any validation errors.

### Running Tests

To run validation tests against all example files:

```bash
python utils/validator.py --test
```

This will:
1. Validate all JSON files in the `examples` directory
2. Create and validate an intentionally invalid example to demonstrate error detection
3. Show detailed validation errors if any files fail validation

### Using the Validator in Code

You can also use the validator in your own Python code:

```python
from utils.validator import AnalogGearValidator

def validate_my_unit(unit_data):
    validator = AnalogGearValidator()
    is_valid, errors = validator.validate_unit(unit_data)
    
    if is_valid:
        print("Unit is valid")
    else:
        print("Validation errors:", validator.format_errors(errors))
```

### Continuous Integration

This repository includes a GitHub Action that automatically validates all unit files whenever changes are made to the `units/` directory, the schema files, or the validator itself. The workflow will:

1. Run on pushes to the main branch that affect relevant files
2. Run on pull requests to the main branch that affect relevant files
3. Can be manually triggered through the GitHub Actions interface

If validation fails, the GitHub Action will report an error, preventing invalid units from being merged into the main branch.

### Git Hooks

This repository includes Git hooks that can be installed locally to help maintain code quality:

- **pre-commit**: Validates unit files before committing and automatically regenerates the units index

To install the hooks, run:

```bash
./hooks/install.sh
```

See the [hooks README](hooks/README.md) for more details on how the hooks work and how to install them manually.

## Usage

This schema can be used to:

1. Create standardized representations of analog hardware
2. Build UI interfaces that accurately render these controls
3. Save and recall settings across different platforms
4. Exchange settings between different applications

To validate your JSON against these schemas, you can use tools like:
- [AJV](https://ajv.js.org/)
- [JSONSchema.net](https://www.jsonschema.net/)
- [JSON Schema Validator](https://www.jsonschemavalidator.net/)

## License

[MIT License](LICENSE) 