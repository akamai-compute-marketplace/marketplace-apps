#!/usr/bin/env bash

################################################################################
# Description:
#   This script formats and lints shell scripts in your project using shfmt
#   and shellcheck.
#
#   Formatting is done in-place using shfmt.
#   Linting is performed with shellcheck.
#   Any shellcheck errors/warnings will be shown in the output.
#   The script exits nonzero if any file fails linting.
#
# Requirements:
#   - shfmt and shellcheck must be installed and available on your PATH.
#
# Installation:
#   Refer to the official documentation for installation instructions:
#     - shfmt:      https://github.com/mvdan/sh/blob/master/cmd/shfmt/README.md
#     - shellcheck: https://github.com/koalaman/shellcheck#installation
#
# Usage:
#   To format and lint all shell scripts in the project recursively:
#     ./check_shell_scripts.sh all
#
#   To format and lint a specific shell script:
#     ./check_shell_scripts.sh path/to/file.sh
#
#   The script will overwrite files with shfmt formatting,
#   then run shellcheck for linting.
#
#   Example:
#     ./check_shell_scripts.sh all
#     ./check_shell_scripts.sh myscript.sh
################################################################################

set -euo pipefail

RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
NC=$(tput sgr0)

usage() {
	echo "Usage:"
	echo "  $0 all             # Format and lint all *.sh files (recursive)"
	echo "  $0 path/to/file.sh # Format and lint a specific shell script"
}

if [[ $# -ne 1 ]]; then
	usage
	exit 1
fi

if [[ "$1" == "all" ]]; then
	sh_files=$(find . -type f -name "*.sh")
	if [ -z "$sh_files" ]; then
		echo "${RED}No shell scripts found.${NC}"
		exit 0
	fi

	echo "${GREEN}Formatting all shell scripts with shfmt...${NC}"
	shfmt -w "$sh_files"

	echo "${GREEN}Linting all shell scripts with shellcheck...${NC}"
	shellcheck_errors=0
	for file in $sh_files; do
		if ! shellcheck "$file"; then
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
elif [[ -f "$1" && "$1" == *.sh ]]; then
	file="$1"
	echo "${GREEN}Formatting $file with shfmt...${NC}"
	shfmt -w "$file"

	echo "${GREEN}Linting $file with shellcheck...${NC}"
	if shellcheck "$file"; then
		echo "${GREEN}File '$file' passed formatting and linting!${NC}"
		exit 0
	else
		echo "${RED}File '$file' failed shellcheck. See output above.${NC}"
		exit 1
	fi
else
	usage
	exit 1
fi
