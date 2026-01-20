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
    echo "  $0 all               # Auto-format and lint all *.yml and *.yaml files recursively"
    echo "  $0 path/to/file.yml  # Auto-format and lint a specific YAML file"
}

if [[ $# -ne 1 ]]; then
    usage
    exit 1
fi

if [[ "$1" == "all" ]]; then
    yaml_files=$(find . -type f \( -name "*.yml" -o -name "*.yaml" \))
    if [ -z "$yaml_files" ]; then
        echo "${RED}No YAML files (*.yml, *.yaml) found.${NC}"
        exit 0
    fi

    echo "${GREEN}Auto-formatting all YAML files with yamlfix...${NC}"
    for file in $yaml_files; do
        echo "${GREEN}Auto-formatting $file with yamlfix...${NC}"
        if ! yamlfix --config-file "$YAMLFIX_CONFIG" "$file"; then
            echo "${RED}yamlfix failed on $file${NC}" >&2
            exit 1
        fi
    done

    echo "${GREEN}Linting all YAML files with yamllint...${NC}"
    lint_errors=0
    for file in $yaml_files; do
        echo "${GREEN}Linting $file with yamllint...${NC}"
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
elif [[ -f "$1" && ( "$1" == *.yml || "$1" == *.yaml ) ]]; then
    file="$1"
    echo "${GREEN}Auto-formatting $file with yamlfix...${NC}"
    if ! yamlfix --config-file "$YAMLFIX_CONFIG" "$file"; then
        echo "${RED}yamlfix failed on $file${NC}" >&2
        exit 1
    fi

    echo "${GREEN}Linting $file with yamllint...${NC}"
    if yamllint -c "$YAMLLINT_CONFIG" "$file"; then
        echo "${GREEN}File '$file' passed yamllint!${NC}"
        exit 0
    else
        echo "${RED}File '$file' failed yamllint. See output above.${NC}"
        exit 1
    fi
else
    usage
    exit 1
fi