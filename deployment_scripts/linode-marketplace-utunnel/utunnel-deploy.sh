#!/bin/bash
set -e
trap "cleanup $? $LINENO" EXIT
 
 
# git repo
export GIT_REPO="https://github.com/akamai-compute-marketplace/marketplace-apps.git"
export WORK_DIR="/tmp/marketplace-apps" 
export MARKETPLACE_APP="apps/linode-marketplace-utunnel"
 
# enable logging
exec > >(tee /dev/ttyS0 /var/log/stackscript.log) 2>&1
 
function cleanup {
  if [ -d "${WORK_DIR}" ]; then
    rm -rf ${WORK_DIR}
  fi
}
 
 
function run {
  echo ">> Updating and installing prerequisites"
  apt-get update
  apt-get install -y git python3 python3-pip python3-virtualenv python3-full
 
  echo ">> Cloning repository"
  git clone ${GIT_REPO} ${WORK_DIR}
 

  echo ">> Entering app directory"
  cd ${WORK_DIR}/${MARKETPLACE_APP}
 
  echo ">> Creating Python virtual environment"
  python3 -m virtualenv env
  source env/bin/activate
 
  echo ">> Installing Python dependencies"
  pip install --upgrade pip
  pip install -r requirements.txt
  ansible --version
  echo ">> Installing Ansible collections"
  ansible-galaxy install -r collections.yml
 
  echo ">> Running Ansible Playbooks"
  ansible-playbook -v site.yml
} 
# main
run
cleanup
