# YAML Linting & Formatting Utilities

This folder contains scripts and configuration files to automatically **format** and **lint** YAML (`.yml`/`.yaml`) files.

- **yamlfix** is an automatic _formatter_ for YAML files. It rewrites your YAML to be consistently indented, spaced, and ordered according to best practices and your configuration. It helps keep YAML files readable and style-consistent.

- **yamllint** is a _linter_ for YAML files. It checks for syntax errors, formatting issues, and violations of YAML style guides or project rules. It helps catch errors and enforces good practices before your YAML files are used by other tools or systems.

## Requirements
Install the required tools:
   - [yamllint](https://github.com/adrienverge/yamllint#installation)
   - [yamlfix](https://github.com/lyz-code/yamlfix#installation)

## How to Use
**Running the script:**

   - To check all YAML files recursively:
     ```sh
     ./check_yaml_scripts.sh all
     ```
   - To check a specific file:
     ```sh
     ./check_yaml_scripts.sh path/to/file.yaml
     ```

   The script will:
   - Auto-format files with yamlfix using `.yamlfix.toml` from this folder
   - Lint them with yamllint using `.yamllint.yml` from this folder
   - Report and stop if any file fails the lint

## Configuration

- **yamlfix** reads its configuration from a file named `.yamlfix.toml`
- **yamllint** reads its rules from a file named `.yamllint.yml`

For more details on each tool's configuration options, see:
- yamllint: [https://yamllint.readthedocs.io/en/stable/configuration.html](https://yamllint.readthedocs.io/en/stable/configuration.html)
- yamlfix: [https://github.com/lyz-code/yamlfix#configuration](https://github.com/lyz-code/yamlfix#configuration)