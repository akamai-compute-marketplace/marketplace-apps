#!/bin/bash
set -e
trap "cleanup $? $LINENO" EXIT

##Linode/SSH security settings
#<UDF name="user_name" label="The limited sudo user to be created for the Linode: *No Capital Letters or Special Characters*" default="ziggy">
#<UDF name="disable_root" label="Disable root access over SSH?" oneOf="Yes,No" default="No">

## NetFoundry Edge Router Settings 
#<UDF name="registration_key" label="Edge Router Registration key" default="none">

# git repo
export GIT_REPO="https://github.com/akamai-compute-marketplace/marketplace-apps.git"
export WORK_DIR="/tmp/marketplace-apps" 
export MARKETPLACE_APP="apps/linode-marketplace-netfoundry-edge-router"
#export BRANCH="feature/netfoundry-edge-router"

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

  # sudo username
  username: ${USER_NAME}
  # registration key
  registration_key: ${REGISTRATION_KEY}

EOF

  if [ "$DISABLE_ROOT" = "Yes" ]; then
    echo "disable_root: yes" >> ${group_vars};
  else echo "Leaving root login enabled";
  fi

}

function run {
  # install dependancies
  apt-get update
  apt-get install -y git python3 python3-pip python3-virtualenv

  # clone repo and set up ansible environment
  git -C /tmp clone ${GIT_REPO}
  # for a single testing branch
  #git -C /tmp clone --single-branch --branch ${BRANCH} ${GIT_REPO}

  # venv
  cd ${WORK_DIR}/${MARKETPLACE_APP}
  python3 -m virtualenv env
  source env/bin/activate
  pip install pip --upgrade
  pip install -r requirements.txt
 
  # populate group_vars
  udf

  # run playbooks
  ansible-playbook -v provision.yml && ansible-playbook -v site.yml
  
}

function installation_complete {
  echo "Installation Complete"
}
# main
run && installation_complete
cleanup
