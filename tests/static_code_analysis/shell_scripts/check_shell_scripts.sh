#!/usr/bin/env bash

SHELLCHECK_OPTS="--exclude=SC1091,SC2154,SC2086 --severity=style"
# SC1091: Not following: (error message here)
# SC2154: var is referenced but not assigned.
# SC2086: Double quote to prevent globbing and word splitting.

set -euo pipefail

RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
NC=$(tput sgr0)

usage() {
	echo "Usage:"
	echo "  $0 path/to/directory    # Format and lint all *.sh files under specified directory"
	echo "  $0 path/to/file.sh      # Format and lint a specific shell script"
}

lint_and_format_file() {
	local file="$1"
	echo "${GREEN}Formatting $file with shfmt...${NC}"
	shfmt -w "$file"

	echo "${GREEN}Linting $file with shellcheck...${NC}"
	if shellcheck $SHELLCHECK_OPTS "$file"; then
		echo "${GREEN}File '$file' passed formatting and linting!${NC}"
		return 0
	else
		echo "${RED}File '$file' failed shellcheck. See output above.${NC}"
		return 1
	fi
}

lint_and_format_files() {
	local files=("$@")
	if [ ${#files[@]} -eq 0 ]; then
		echo "${RED}No shell scripts found.${NC}"
		exit 0
	fi

  echo "${GREEN}Formatting files with shfmt...${NC}"
	shfmt -w "${files[@]}"

	echo "${GREEN}Linting files with shellcheck...${NC}"
	shellcheck_errors=0
	for file in "${files[@]}"; do
		if ! shellcheck $SHELLCHECK_OPTS "$file"; then
			echo "${RED}shellcheck - issue found in $file${NC}"
			shellcheck_errors=1
		fi
	done

	if [[ $shellcheck_errors -eq 0 ]]; then
		echo "${GREEN}All shell scripts passed linting!${NC}"
		exit 0
	else
		echo "${RED}Some scripts failed shellcheck. See output above.${NC}"
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
	done < <(find "$1" -type f -name "*.sh")
	lint_and_format_files "${files[@]}"
elif [[ -f "$1" && "$1" == *.sh ]]; then
	lint_and_format_file "$1"
else
	usage
	exit 1
fi
