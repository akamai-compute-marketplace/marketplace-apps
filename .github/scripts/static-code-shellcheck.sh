#!/usr/bin/env bash

set -e

sudo apt-get update
sudo apt-get install -y shellcheck
find . -type f -name "*.sh" -print0 | xargs -0 shellcheck --severity=error --exclude=SC1091,SC2154,SC2086,SC1071
echo "✅ ShellCheck passed: no error-level issues found."
