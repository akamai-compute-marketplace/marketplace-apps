#!/usr/bin/env bash

YAMLLINT_CONFIG="tests/static_code_analysis/yaml_configs/.yamllint.yml"

set -euo pipefail

RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
NC=$(tput sgr0)

usage() {
    echo "Usage:"
    echo "  $0 path/to/dir       # Lint all *.yml and *.yaml files recursively in directory"
    echo "  $0 path/to/file.yml  # Lint a specific YAML file"
}

lint_and_format() {
  local path="$1"

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