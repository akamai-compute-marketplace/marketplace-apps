#!/usr/bin/env bash

set -e

pip install ansible-lint
echo -e '[defaults]\ndeprecation_warnings = False' >ansible.cfg
ansible-galaxy collection install community.general community.docker community.postgresql community.crypto community.mysql community.mongodb
ansible-lint -c tests/static_code_analysis/ansible_playbooks/.ansible-lint.yaml
echo "✅ ansible-lint passed: no errors found."
