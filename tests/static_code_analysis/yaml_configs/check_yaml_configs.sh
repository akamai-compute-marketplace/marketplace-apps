#!/usr/bin/env bash

CONFIG_DIR="tests/static_code_analysis/yaml_configs"
YAMLLINT_CONFIG="$CONFIG_DIR/.yamllint.yml"
YAMLFIX_CONFIG="$CONFIG_DIR/.yamlfix.toml"

set -euo pipefail

RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
NC=$(tput sgr0)

usage() {
    echo "Usage:"
    echo "  $0 path/to/dir       # Auto-format and lint all *.yml and *.yaml files recursively in directory"
    echo "  $0 path/to/file.yml  # Auto-format and lint a specific YAML file"
}

lint_and_format() {
  local path="$1"
  echo "${GREEN}Auto-formatting with yamlfix...${NC}"
  yamlfix --config-file "$YAMLFIX_CONFIG" "$path"

  echo "${GREEN}Linting with yamllint...${NC}"
  if yamllint -c "$YAMLLINT_CONFIG" "$path"; then
    echo "${GREEN}yamllint passed!${NC}"
    return 0
  else
    echo "${RED}yamllint failed. See output above.${NC}"
    return 1
  fi
}

if [[ $# -ne 1 ]]; then
    usage
    exit 1
fi

lint_and_format "$1"