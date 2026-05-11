#!/bin/bash

set -e

TEST_PATH="tests/regression_tests/apps/$APP_NAME/test_scenarios.py"

if [ -f "$TEST_PATH" ]; then
  python -m pip install --upgrade pip
  pip install -r tests/regression_tests/requirements.txt
  playwright install chromium --with-deps
  mkdir -p reports/screenshots
  pytest "$TEST_PATH" --html=reports/report.html --self-contained-html --tb=short -q -rN
else
  echo "Test file $TEST_PATH not found. Skipping tests for $APP_NAME."
  exit 0
fi
