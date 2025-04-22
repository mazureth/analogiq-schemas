# Analog Gear Schema Git Hooks

This directory contains Git hooks to help maintain code quality and consistency in the repository.

## Available Hooks

### pre-commit

The pre-commit hook automatically runs the schema validator on any unit files (JSON files in the `units/` directory) that are being committed. If any validation errors are found, the commit is aborted.

Additionally, the hook will automatically regenerate the `units/index.json` file when unit files are modified, ensuring that the index is always up-to-date.

## Installation

To install the hooks, run the installation script:

```bash
./hooks/install.sh
```

This will install the hooks in your local `.git/hooks` directory.

## Manual Installation

If you prefer to install the hooks manually:

1. Copy the hook scripts to your `.git/hooks` directory:
   ```bash
   cp hooks/pre-commit .git/hooks/
   ```

2. Make sure the scripts are executable:
   ```bash
   chmod +x .git/hooks/pre-commit
   ```

## Features

The pre-commit hook:

1. Only validates unit files that are staged for commit
2. Skips the `units/index.json` file to avoid validation issues
3. Provides colorful output indicating which files passed or failed validation
4. Regenerates the `units/index.json` file if any unit files were modified
5. Automatically stages the updated index file

## Troubleshooting

### Bypassing Hooks

If you need to bypass the hooks for a specific commit, you can use the `--no-verify` flag:

```bash
git commit --no-verify -m "Your commit message"
```

However, this is not recommended as it skips the validation process.

### Hook Not Running

If the hooks aren't running, check:

1. Are the hook scripts executable? (`chmod +x hooks/pre-commit`)
2. Are the hooks properly installed in `.git/hooks/`?
3. Do the hooks have the correct name (no file extension in `.git/hooks/`)? 