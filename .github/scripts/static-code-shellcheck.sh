#!/usr/bin/env bash

set -e

sudo apt-get update
sudo apt-get install -y shellcheck
find . -type f -name "*.sh" -print0 | xargs -0 shellcheck --severity=error
echo "✅ ShellCheck passed: no error-level issues found."
