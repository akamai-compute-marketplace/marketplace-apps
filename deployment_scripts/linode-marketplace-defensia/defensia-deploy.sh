#!/bin/bash
# enable logging
exec > >(tee /dev/ttyS0 /var/log/stackscript.log) 2>&1

# trap cleanup
trap "cleanup $? $LINENO" EXIT

## Defensia Marketplace App Deployment Script

### set variables
GIT_REPO="https://github.com/akamai-compute-marketplace/marketplace-apps.git"
WORK_DIR="/root/repo"
MARKETPLACE_APP="apps/linode-marketplace-defensia"
BRANCH="${BRANCH:-main}"

function cleanup {
  if [ "$1" != "0" ]; then
    echo "Error occurred (exit code $1) at line $2"
  fi
}

function udf {
  local group_vars="${WORK_DIR}/${MARKETPLACE_APP}/group_vars/linode/vars"

  # TOKEN may be empty in CI/staging — Ansible handles validation
  echo "token: ${TOKEN:-}" >> "${group_vars}"

  if [[ -n "${AGENT_NAME}" ]]; then
    echo "agent_name: ${AGENT_NAME}" >> "${group_vars}"
  else
    echo "agent_name: $(hostname -s)" >> "${group_vars}"
  fi

  # mode: staging in CI, production otherwise
  echo "mode: ${MODE:-production}" >> "${group_vars}"
}

function run {
  # install dependencies
  apt-get update -q
  apt-get install -yq git python3 python3-pip python3-venv

  # clone repo
  git clone -b "${BRANCH}" "${GIT_REPO}" "${WORK_DIR}"

  # setup ansible environment
  cd "${WORK_DIR}/${MARKETPLACE_APP}"
  python3 -m venv env
  source env/bin/activate
  pip install -r requirements.txt
  ansible-galaxy collection install -r collections.yml

  # populate group_vars with UDF variables
  udf

  # run playbooks
  ansible-playbook -v provision.yml
  ansible-playbook -v site.yml
}

run
