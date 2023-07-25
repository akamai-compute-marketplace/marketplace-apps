#!/bin/bash
set -e
trap "cleanup $? $LINENO" EXIT

## MainConcept MC2GO P2 AVC Ultra Transcoder Demo Settings
#<UDF name="mc2go_port" Label="MC2GO P2 AVC Ultra Transcoder Port" example="Default: 8080" default="8080" /> 

# git repo
#export GIT_REPO="https://github.com/linode-solutions/marketplace-apps.git"

#test git repo
export GIT_REPO="https://github.com/jongov/marketplace-apps.git"
export BRANCH="develop"

export WORK_DIR="/tmp/marketplace-apps"
export MARKETPLACE_APP="apps/linode-marketplace-mc2go-p2-avc-demo"

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

  # deployment vars
  mc2go_port: ${MC2GO_PORT}
EOF

}

function run {
  # install dependancies
  apt-get update
  apt-get install -y git python3 python3-pip

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