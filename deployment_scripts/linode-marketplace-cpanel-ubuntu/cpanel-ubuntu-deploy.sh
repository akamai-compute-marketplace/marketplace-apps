#!/bin/bash
set -e
# STACKSCRIPT_ID: 595742
# enable logging
exec > >(tee /dev/ttyS0 /var/log/stackscript.log) 2>&1

# cleanup will always happen. If DEBUG is passed and is anything
# other than NO, it will always trigger cleanup. This is useful for
# ci testing and passing vars to the instance.

#DEBUG="NO"
if [[ -n ${DEBUG} ]]; then
  if [ "${DEBUG}" == "NO" ]; then
    trap "cleanup $? $LINENO" EXIT
  fi
else
  trap "cleanup $? $LINENO" EXIT
fi

#GH_USER=""
#BRANCH=""
# git user and branch
if [[ -n ${GH_USER} && -n ${BRANCH} ]]; then
        echo "[info] git user and branch set.."
        export GIT_REPO="https://github.com/${GH_USER}/marketplace-apps.git"

else
        export GH_USER="akamai-compute-marketplace"
        export BRANCH="main"
        export GIT_REPO="https://github.com/${GH_USER}/marketplace-apps.git"
fi

export WORK_DIR="/root/marketplace-apps" # moved to root dir because cpanel install will remove anything in tmp

function cleanup {
  if [ -d "${WORK_DIR}" ]; then
    rm -rf ${WORK_DIR}
  fi

}
 
# Check if /etc/os-release file exists
if [ -f /etc/os-release ]; then
    # Source the os-release file to get the distribution ID
    . /etc/os-release

    # Check the distribution ID to determine the Linux distribution
    if [ "$ID" == "almalinux" ]; then
        export MARKETPLACE_APP="apps/linode-marketplace-cpanel-almalinux"

        function run {
        # install dependancies
        yum install dnf -y
        dnf update -y
        dnf upgrade -y
        dnf install -y git python3 python3-pip

        dnf makecache
        dnf install epel-release -y
        dnf makecache
        }

    elif [ "$ID" == "ubuntu" ]; then
        export MARKETPLACE_APP="apps/linode-marketplace-cpanel-ubuntu"
        
        function run {
        # install dependancies
        export DEBIAN_FRONTEND=non-interactive
        apt-get update
        apt-get install -y git python3 python3-pip python3-venv
        }

    else
        echo "Unknown Linux distribution: $ID"
    fi
else
    echo "Unable to determine the Linux distribution."
fi

function udf {
  local group_vars="${WORK_DIR}/${MARKETPLACE_APP}/group_vars/linode/vars"
}  

function final_run {
  # clone repo and set up ansible environment
  git -C /root clone -b ${BRANCH} ${GIT_REPO}
  # for a single testing branch
  # git -C /root clone -b ${BRANCH} ${GIT_REPO}

  # venv
  cd ${WORK_DIR}/${MARKETPLACE_APP}
  python3 -m venv env
  source env/bin/activate
  pip install pip --upgrade
  pip install -r requirements.txt
  ansible-galaxy install -r collections.yml

  # populate group_vars
  udf

  # run playbook
  ansible-playbook -v site.yml
}

function installation_complete {
  echo "Installation Complete"
}
# main
run
final_run
installation_complete