#!/usr/bin/env python3
"""
Analog Gear Index Generator

Generates an index.json file containing metadata about all available units
"""

import json
import os
import sys
import re
from pathlib import Path


class IndexGenerator:
    """Generates an index of available analog gear units"""

    def __init__(self):
        """Initialize the generator with paths"""
        # Get the root directory (parent of utils)
        self.root_dir = Path(__file__).parent.parent
        self.units_dir = self.root_dir / "units"
        self.output_file = self.units_dir / "index.json"

        # Compiled regex for filename versioning
        self.version_pattern = re.compile(r"^(.+)-(\d+\.\d+\.\d+)\.json$")

    def scan_units(self):
        """
        Scan the units directory for all unit files and extract metadata

        Returns:
            List of dictionaries containing unit metadata
        """
        units = []

        if not self.units_dir.exists():
            print(f"Error: Units directory not found at {self.units_dir}")
            return units

        for file_path in self.units_dir.glob("*.json"):
            try:
                # Check if the filename matches the expected pattern
                filename_match = self.version_pattern.match(file_path.name)
                if not filename_match:
                    print(
                        f"Warning: Skipping file with invalid name format: {file_path.name}"
                    )
                    continue

                # Extract data from the file
                with open(file_path, "r") as f:
                    unit_data = json.load(f)

                # Extract required metadata
                unit_info = {
                    "unitId": unit_data.get("unitId"),
                    "name": unit_data.get("name"),
                    "category": unit_data.get("category"),
                    "version": unit_data.get("version"),
                    "schemaPath": str(file_path.relative_to(self.root_dir)),
                    "thumbnailImage": unit_data.get("thumbnailImage"),
                }

                # Validate that we have all required fields
                if not all(unit_info.values()):
                    missing = [k for k, v in unit_info.items() if not v]
                    print(
                        f"Warning: Unit {file_path.name} is missing required fields: {', '.join(missing)}"
                    )
                    continue

                units.append(unit_info)
                print(f"Added {unit_info['name']} to index")

            except Exception as e:
                print(f"Error processing {file_path.name}: {e}")

        return units

    def generate_index(self):
        """
        Generate the index.json file

        Returns:
            bool: True if successful, False otherwise
        """
        units = self.scan_units()

        if not units:
            print("No valid units found, index not generated")
            return False

        # Sort units by category and then by name
        units.sort(key=lambda x: (x["category"], x["name"]))

        try:
            with open(self.output_file, "w") as f:
                json.dump({"units": units}, f, indent=4)

            print(
                f"Successfully generated index with {len(units)} units at {self.output_file}"
            )
            return True

        except Exception as e:
            print(f"Error generating index file: {e}")
            return False


def main():
    """Main function for the index generator script"""
    generator = IndexGenerator()
    success = generator.generate_index()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
