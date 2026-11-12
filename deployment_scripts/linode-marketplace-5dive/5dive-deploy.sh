#!/bin/bash
# STACKSCRIPT_ID: (assigned by Akamai on acceptance)

# enable logging
set -e
exec > >(tee /dev/ttyS0 /var/log/stackscript.log) 2>&1

#DEBUG="NO"
# cleanup will always happen. If DEBUG is passed and is anything
# other than NO, it will always trigger cleanup. This is useful for
# ci testing and passing vars to the instance.

if [[ -n ${DEBUG} ]]; then
  if [ "${DEBUG}" == "NO" ]; then
    trap "cleanup $? $LINENO" EXIT
  fi
else
  trap "cleanup $? $LINENO" EXIT
fi

## Linode/SSH security settings
#<UDF name="user_name" label="The limited sudo user to be created for the Linode: *No Capital Letters or Special Characters*">
#<UDF name="disable_root" label="Disable root access over SSH?" oneOf="Yes,No" default="No">

## Addons
#<UDF name="add_ons" label="Optional data exporter Add-ons for your deployment" manyOf="node_exporter,mysqld_exporter,newrelic,none" default="none">

#GH_USER=""
#BRANCH=""
# git user and branch
if [[ -n ${GH_USER} && -n ${BRANCH} ]]; then
  echo "[info] git user and branch set.."
else
  export GH_USER="akamai-compute-marketplace"
  export BRANCH="main"
fi
export GIT_REPO="https://github.com/${GH_USER}/marketplace-apps.git"

export WORK_DIR="/tmp/marketplace-apps"
export MARKETPLACE_APP="apps/linode-marketplace-5dive"

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
  default_dns: $(hostname -I | awk '{print $1}' | tr '.' '-' | awk '{print $1 ".ip.linodeusercontent.com"}')
  # addons
  add_ons: [${ADD_ONS}]
EOF

  if [ "$DISABLE_ROOT" = "Yes" ]; then
    echo "disable_root: yes" >> ${group_vars}
  else
    echo "Leaving root login enabled"
  fi
}

function run {
  # install dependencies
  apt-get update
  apt-get install -y git python3 python3-pip python3-venv

  # clone the repo and set up ansible
  git -C /tmp clone --recurse-submodules -b ${BRANCH} ${GIT_REPO}
  cd ${WORK_DIR}/${MARKETPLACE_APP}
  python3 -m venv env
  source env/bin/activate
  pip install pip --upgrade
  pip install -r requirements.txt
  ansible-galaxy install -r collections.yml

  # populate group_vars
  udf
  # run playbooks
  ansible-playbook -v provision.yml && ansible-playbook -v site.yml
}

function installation_complete {
  echo "Installation Complete"
}

# main
run
installation_complete
