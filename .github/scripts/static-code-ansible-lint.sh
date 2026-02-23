#!/usr/bin/env bash

set -e

pip install ansible-lint
ansible-galaxy collection install community.general community.docker community.postgresql community.crypto community.mysql community.mongodb
export ANSIBLE_CONFIG="tests/static_code_analysis/ansible_playbooks/ansible.cfg"
ansible-lint -c tests/static_code_analysis/ansible_playbooks/.ansible-lint.yaml
echo "✅ ansible-lint passed: no errors found."
