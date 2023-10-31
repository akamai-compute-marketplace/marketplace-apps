#!/bin/bash
set -e
trap "cleanup $? $LINENO" EXIT

# git repo
export GIT_REPO="https://github.com/akamai-compute-marketplace/marketplace-apps.git"
export WORK_DIR="/root/marketplace-apps" # moved to root dir because cpanel install will remove anything in tmp
export MARKETPLACE_APP="apps/linode-marketplace-cpanel-almalinux"

# enable logging
exec > >(tee /dev/ttyS0 /var/log/stackscript.log) 2>&1

function cleanup {
  if [ -d "${WORK_DIR}" ]; then
    rm -rf ${WORK_DIR}
  fi

}

function run {
  # install dependancies
  yum install dnf -y
  dnf update -y
  dnf upgrade -y
  dnf install -y git python3 python3-pip

  dnf makecache
  dnf install epel-release -y
  dnf makecache
  dnf install ansible -y

  # clone repo and set up ansible environment
  git -C /root clone ${GIT_REPO}
  # for a single testing branch
  # git -C /root clone -b ${BRANCH} ${GIT_REPO}

  # venv
  cd ${WORK_DIR}/${MARKETPLACE_APP}
  pip3 install virtualenv
  python3 -m virtualenv env
  source env/bin/activate
  pip install pip --upgrade
  pip install -r requirements.txt
  ansible-galaxy install -r collections.yml

  # run playbook
  ansible-playbook -v site.yml
}

function installation_complete {
  echo "Installation Complete"
}
# main
run && installation_complete
cleanup
