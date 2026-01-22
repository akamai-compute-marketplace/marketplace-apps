# YAML Linting & Formatting Utilities

This folder contains scripts and configuration files to automatically **format** and **lint** YAML (`.yml`/`.yaml`) files.

- **yamllint** is a _linter_ for YAML files. It checks for syntax errors, formatting issues, and violations of YAML style guides or project rules. 
- It helps catch errors and enforces good practices before your YAML files are used by other tools or systems.

## Requirements
Install the required tools:
   - [yamllint](https://github.com/adrienverge/yamllint#installation)

## How to Use
**Running the script:**

**Lint all YAML files under specified directory:**
```sh
./check_yaml_configs.sh path/to/directory
```

**Lint a specific YAML file:**
```sh
./check_yaml_configs.sh path/to/script.sh
```

## Configuration

- **yamllint** reads its rules from a file named `.yamllint.yml`

For more details on each tool's configuration options, see:
- yamllint: [https://yamllint.readthedocs.io/en/stable/configuration.html](https://yamllint.readthedocs.io/en/stable/configuration.html)
