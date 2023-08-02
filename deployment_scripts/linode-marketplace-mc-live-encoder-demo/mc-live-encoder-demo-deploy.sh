#!/bin/bash

set -e
trap "cleanup $? $LINENO" EXIT

# git repo
#export GIT_REPO="https://github.com/linode-solutions/marketplace-apps.git"

#test git repo
export GIT_REPO="https://github.com/jongov/marketplace-apps.git"
export BRANCH="develop"

export WORK_DIR="/tmp/marketplace-apps"
export MARKETPLACE_APP="apps/linode-marketplace-mc-live-encoder-demo"

# enable logging
exec > >(tee /dev/ttyS0 /var/log/stackscript.log) 2>&1

function cleanup {
  if [ -d "${WORK_DIR}" ]; then
    rm -rf ${WORK_DIR}
  fi

}

function udf {
  local group_vars="${WORK_DIR}/${MARKETPLACE_APP}/group_vars/linode/vars"
  sed 's/  //g' <<EOF > ${group_vars}
EOF

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
  # git -C /tmp clone ${GIT_REPO}
  # for a single testing branch
  git -C /tmp clone --single-branch --branch ${BRANCH} ${GIT_REPO}

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
  for playbook in provision.yml site.yml; do ansible-playbook -vvvv $playbook; done
}

function installation_complete {
  # dumping credentials  
  echo -e "username=admin\npassword=admin" > /root/.linode_credentials.txt
  cat << EOF
#########################
# INSTALLATION COMPLETE #
############################################
# * Hugs are worth more than handshakes *  #
############################################
EOF
}
# main
run && installation_complete
cleanup
