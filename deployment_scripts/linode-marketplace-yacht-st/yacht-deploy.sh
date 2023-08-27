#!/bin/bash
set -e
trap "cleanup $? $LINENO" EXIT

## Yacht Settings 
#<UDF name="YEMAIL" Label="Yacht Email" example="admin@yacht.local" default="admin@yacht.local" />
#<UDF name="YPASSWORD" Label="Yacht Password" example="Password" />
#<UDF name="COMPOSE_SUPPORT" Label="Yacht Compose Support" example="Yes" default="Yes" oneof="Yes,No" />
#<UDF name="YACHT_THEME" Label="Yacht Theme" example="Default" default="Default" oneof="Default,RED,OMV" />

# git repo
export GIT_REPO="https://github.com/jcotoBan/marketplace-apps.git"
export WORK_DIR="/tmp/marketplace-apps" 
export MARKETPLACE_APP="apps/linode-marketplace-yacht"

# enable logging
exec > >(tee /dev/ttyS0 /var/log/stackscript.log) 2>&1

function cleanup {
  if [ -d "${WORK_DIR}" ]; then
    rm -rf ${WORK_DIR}
  fi

}

function udf {
  local group_vars="${WORK_DIR}/${MARKETPLACE_APP}/group_vars/linode/vars"
  
  if [[ -n ${YEMAIL} ]]; then
    echo "yemail: ${YEMAIL}" >> ${group_vars};
  fi

  if [[ -n ${YPASSWORD} ]]; then
    echo "ypassword: ${YPASSWORD}" >> ${group_vars};
  fi

  if [[ -n ${COMPOSE_SUPPORT} ]]; then
    echo "compose_support: '${COMPOSE_SUPPORT}'" >> ${group_vars};
  fi

  if [[ -n ${YACHT_THEME} ]]; then
    echo "yacht_theme: ${YACHT_THEME}" >> ${group_vars};
  fi
}

function run {
  # install dependancies
  apt-get update
  apt-get install -y git python3 python3-pip

  # clone repo and set up ansible environment
  git -C /tmp clone ${GIT_REPO}
  # for a single testing branch
  # git -C /tmp clone --single-branch --branch ${BRANCH} ${GIT_REPO}

  # venv
  cd ${WORK_DIR}/${MARKETPLACE_APP}
  pip3 install virtualenv
  python3 -m virtualenv env
  source env/bin/activate
  pip install pip --upgrade
  pip install -r requirements.txt
  ansible-galaxy install -r collections.yml

  # populate group_vars
  udf
  # run playbooks
  for playbook in site.yml; do ansible-playbook -vvvv $playbook; done
  #Remeber to ask what provision.yml in this case is doing?
}

function installation_complete {
  echo "Installation Complete"
}
# main
run && installation_complete
cleanup
