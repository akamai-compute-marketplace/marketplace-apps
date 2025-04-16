#!/bin/bash
set -e
if [ "${DEBUG}" == "NO" ]; then
  trap "cleanup $? $LINENO" EXIT
fi

## Kali
#<UDF name="everything" label="Would you like to Install the Kali Everything Package?" oneOf="Yes,No" default="Yes">
#<UDF name="headless" label="Would you like to Install the Kali Headless Package?" oneOf="Yes,No" default="No">
#<UDF name="vnc" label="Would you like to setup VNC to access Kali XFCE Desktop" oneOf="Yes,No" default="Yes">
#<UDF name="vnc_username" label="The VNC user to be created for the Linode. The username accepts only lowercase letters, numbers, dashes (-) and underscores (_)">
#<UDF name="vnc_password" label="The password for the limited VNC user">

## Linode/SSH Security Settings
#<UDF name="user_name" label="The limited sudo user to be created for the Linode: *All lowercase*">
#<UDF name="disable_root" label="Disable root access over SSH?" oneOf="Yes,No" default="No">

# git repo
export GIT_REPO="https://github.com/akamai-compute-marketplace/marketplace-apps.git"
export WORK_DIR="/tmp/marketplace-apps" 
export MARKETPLACE_APP="apps/linode-marketplace-kali-linux"

# enable logging
exec > >(tee /dev/ttyS0 /var/log/stackscript.log) 2>&1

function cleanup {
  if [ -d "${WORK_DIR}" ]; then
    rm -rf ${WORK_DIR}
  fi

}

function udf {
  # Translate UDF values to boolean variables
  local EVERYTHING_BOOL=false
  local HEADLESS_BOOL=false
  local VNC_BOOL=false
  local DISABLE_ROOT_BOOL=false

  if [ "${EVERYTHING}" == "Yes" ]; then
    EVERYTHING_BOOL=true
  fi

  if [ "${HEADLESS}" == "Yes" ]; then
    HEADLESS_BOOL=true
  fi

  if [ "${VNC}" == "Yes" ]; then
    VNC_BOOL=true
  fi

  if [ "${DISABLE_ROOT}" == "Yes" ]; then
    DISABLE_ROOT_BOOL=true
  fi

  local group_vars="${WORK_DIR}/${MARKETPLACE_APP}/group_vars/linode/vars"

  sed 's/  //g' <<EOF > ${group_vars}
  # Kali Linux settings
  kali_package: "{{ 'kali-linux-everything' if ${EVERYTHING_BOOL} else 'kali-linux-headless' if ${HEADLESS_BOOL} else '' }}"

  # VNC settings
  vnc_enabled: ${VNC_BOOL}
  vnc_username: "${VNC_USERNAME}"
  vnc_password: "${VNC_PASSWORD}"

  # Other variables
  username: "${USER_NAME}"
  disable_root: ${DISABLE_ROOT_BOOL}
  default_dns: "$(hostname -I | awk '{print $1}'| tr '.' '-' | awk {'print $1 ".ip.linodeusercontent.com"'})"
EOF
}

function run {
  # Set debconf to automatically handle service restarts
  echo 'libc6:amd64 libraries/restart-without-asking boolean true' | debconf-set-selections
  echo 'libc6 libraries/restart-without-asking boolean true' | debconf-set-selections
  # install dependencies
  DEBIAN_FRONTEND=noninteractive apt-get update
  DEBIAN_FRONTEND=noninteractive apt-get install -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" \
    git \
    python3 \
    python3-pip \
    python3-venv \
    python3-full \
    ansible
  # clone repo and set up ansible environment
  git -C /tmp clone ${GIT_REPO}
  # for a single testing branch
  # git -C /tmp clone -b ${BRANCH} ${GIT_REPO}

    # venv
  cd ${WORK_DIR}/${MARKETPLACE_APP}
  apt install python3-venv -y
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
run && installation_complete
if [ "${DEBUG}" == "NO" ]; then
  cleanup
fi
