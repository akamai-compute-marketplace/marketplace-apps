#!/bin/bash
set -e
trap "cleanup $? $LINENO" EXIT

## Docker Settings

## Linode/SSH Security Settings
#<UDF name="user_name" label="The limited sudo user to be created for the Linode">
#<UDF name="disable_root" label="Disable root access over SSH?" oneOf="Yes,No" default="No">
#<UDF name="pubkey" label="The SSH Public Key that will be used to access the Linode (Recommended)" default="">

# git repo
export GIT_REPO="https://github.com/akamai-compute-marketplace/marketplace-apps.git"
export WORK_DIR="/tmp/marketplace-apps" 
export MARKETPLACE_APP="apps/linode-marketplace-cloudron"

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
  default_dns: $(hostname -I | awk '{print $1}'| tr '.' '-' | awk {'print $1 ".ip.linodeusercontent.com"'})
EOF
  if [[ -n ${PUBKEY} ]]; then
    echo "pubkey: ${PUBKEY}" >> ${group_vars};
  else echo "No pubkey entered";
  fi

  if [ "$DISABLE_ROOT" = "Yes" ]; then
    echo "disable_root: yes" >> ${group_vars};
  else echo "Leaving root login enabled";
  fi
}

function run {
  # install dependancies
  apt-get update
  apt-get install -y git python3 python3-pip

  # clone repo and set up ansible environment
  git -C /tmp clone ${GIT_REPO}
  # for a single testing branch
  # git -C /tmp clone -b ${BRANCH} ${GIT_REPO}

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
  for playbook in provision.yml site.yml; do ansible-playbook -v $playbook; done
}

function installation_complete {
  echo "Installation Complete"
}
# main
run && installation_complete
cleanup
reboot