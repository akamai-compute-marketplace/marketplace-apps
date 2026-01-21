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

lint_and_format_file() {
  local file="$1"
  echo "${GREEN}Auto-formatting $file with yamlfix...${NC}"
  yamlfix --config-file "$YAMLFIX_CONFIG" "$file"

  echo "${GREEN}Linting $file with yamllint...${NC}"
  if yamllint -c "$YAMLLINT_CONFIG" "$file"; then
    echo "${GREEN}File '$file' passed yamllint!${NC}"
    return 0
  else
    echo "${RED}File '$file' failed yamllint. See output above.${NC}"
    return 1
  fi
}

lint_and_format_files() {
  local files=("$@")
  if [ ${#files[@]} -eq 0 ]; then
    echo "${RED}No YAML files (*.yml, *.yaml) found.${NC}"
    exit 0
  fi

  echo "${GREEN}Auto-formatting files with yamlfix...${NC}"
  for file in "${files[@]}"; do
    echo "${GREEN}Auto-formatting $file with yamlfix...${NC}"
    yamlfix --config-file "$YAMLFIX_CONFIG" "$file"
  done

  echo "${GREEN}Linting all YAML files with yamllint...${NC}"
  lint_errors=0
  for file in "${files[@]}"; do
    if ! yamllint -c "$YAMLLINT_CONFIG" "$file"; then
      echo "${RED}yamllint - issue found in $file${NC}"
      lint_errors=1
    fi
  done

  if [[ $lint_errors -eq 0 ]]; then
    echo "${GREEN}All YAML files auto-formatted and passed yamllint!${NC}"
    exit 0
  else
    echo "${RED}Some YAML files failed yamllint. See output above.${NC}"
    exit 1
  fi
}

if [[ $# -ne 1 ]]; then
    usage
    exit 1
fi

if [[ -d "$1" ]]; then
	files=()
	while IFS= read -r file; do
		files+=("$file")
	done < <(find "$1" -type f \( -name "*.yml" -o -name "*.yaml" \))
	lint_and_format_files "${files[@]}"
elif [[ -f "$1" && "$1" == *.sh ]]; then
	lint_and_format_file "$1"
else
	usage
	exit 1
fi