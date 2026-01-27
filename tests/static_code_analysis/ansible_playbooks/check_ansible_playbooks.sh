#!/usr/bin/env bash

CONFIG_FILE="tests/static_code_analysis/ansible_playbooks/.ansible-lint.yaml"

set -euo pipefail

RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
NC=$(tput sgr0)

usage() {
    echo "Usage:"
    echo "  $0 path/to/file.yml    # Lint a specific Ansible playbook"
    echo "  $0 path/to/directory   # Lint all YAML files in a directory"
}

lint_file() {
    local file="$1"
    echo "${GREEN}Linting $file with ansible-lint...${NC}"
    if ansible-lint -c "$CONFIG_FILE" "$file"; then
        echo "${GREEN}File '$file' passed linting!${NC}"
        return 0
    else
        echo "${RED}File '$file' failed ansible-lint. See output above.${NC}"
        return 1
    fi
}

lint_files() {
    local files=("$@")
    if [ ${#files[@]} -eq 0 ]; then
        echo "${GREEN}No YAML files found to lint.${NC}"
        exit 0
    fi

    echo "${GREEN}Linting files with ansible-lint...${NC}"
    if ansible-lint -c "$CONFIG_FILE" "${files[@]}"; then
        echo "${GREEN}All files passed ansible-lint!${NC}"
        exit 0
    else
        echo "${RED}ansible-lint failed. See output above.${NC}"
        exit 1
    fi
}

if [[ $# -ne 1 ]]; then
    usage
    exit 1
fi

path="$1"

if [[ -d "$path" ]]; then
    files=()
    while IFS= read -r file; do
        files+=("$file")
    done < <(find "$path" -type f \( -name "*.yml" -o -name "*.yaml" \))
    lint_files "${files[@]}"
elif [[ -f "$path" ]]; then
    lint_file "$path"
else
    echo "${RED}Error: '$path' is not a valid file or directory.${NC}"
    usage
    exit 1
fi
