#!/usr/bin/env bash

set -e

pip install yamllint
yamllint -c tests/static_code_analysis/yaml_configs/.yamllint.yml .
echo "✅ yamllint passed: no errors found."
