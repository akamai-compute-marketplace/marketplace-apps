#!/bin/bash

# enable logging
exec > >(tee /dev/ttyS0 /var/log/stackscript.log) 2>&1

# modes
#DEBUG="NO"
if [[ -n ${DEBUG} ]]; then
  if [ "${DEBUG}" == "NO" ]; then
    trap "cleanup $? $LINENO" EXIT
  fi
else
  trap "cleanup $? $LINENO" EXIT
fi

if [ "${MODE}" == "staging" ]; then
  trap "provision_failed $? $LINENO" ERR
else
  set -e
fi

## Akamai Compute/SSH Security Settings
#<UDF name="user_name" label="The limited sudo user to be created for the Akamai Compute Instance: *All lowercase*">
#<UDF name="disable_root" label="Disable root access over SSH?" oneOf="Yes,No" default="No">

## Kali Settings
#<UDF name="kali_package" label="Kali Linux Package" oneOf="Everything,Headless,Core" default="Headless">
#<UDF name="vnc" label="Setup VNC Remote Desktop? (recommended for Everything package; adds desktop to Headless/Core)" oneOf="Yes,No" default="No">
#<UDF name="vnc_username" label="The VNC user to be created for the Akamai Compute Instance. The username accepts only lowercase letters, numbers, dashes (-) and underscores (_)">

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

export WORK_DIR="/tmp/marketplace-apps" 
export MARKETPLACE_APP="apps/linode-marketplace-kali-linux"

function provision_failed {
  echo "[info] Provision failed. Sending status.."

  # dep
  apt install jq -y

  # set token
  local token=($(curl -ks -X POST ${KC_SERVER} \
     -H "Content-Type: application/json" \
     -d "{ \"username\":\"${KC_USERNAME}\", \"password\":\"${KC_PASSWORD}\" }" | jq -r .token) )

  # send pre-provision failure
  curl -sk -X POST ${DATA_ENDPOINT} \
     -H "Authorization: ${token}" \
     -H "Content-Type: application/json" \
     -d "{ \"app_label\":\"${APP_LABEL}\", \"status\":\"provision_failed\", \"branch\": \"${BRANCH}\", \
        \"gituser\": \"${GH_USER}\", \"runjob\": \"${RUNJOB}\", \"image\":\"${IMAGE}\", \
        \"type\":\"${TYPE}\", \"region\":\"${REGION}\", \"instance_env\":\"${INSTANCE_ENV}\" }"
  
  exit $?
}

function cleanup {
  if [ -d "${WORK_DIR}" ]; then
    rm -rf ${WORK_DIR}
  fi
}

function udf {
  local KALI_PACKAGE_NAME=""

  # Set the Kali package name based on selection
  case "${KALI_PACKAGE}" in
    "Everything")
      KALI_PACKAGE_NAME="kali-linux-everything"
      ;;
    "Headless")
      KALI_PACKAGE_NAME="kali-linux-headless"
      ;;
    "Core")
      KALI_PACKAGE_NAME="kali-linux-core"
      ;;
    *)
      KALI_PACKAGE_NAME="kali-linux-headless"  # Default
      ;;
  esac

  local group_vars="${WORK_DIR}/${MARKETPLACE_APP}/group_vars/linode/vars"

  sed 's/  //g' <<EOF > ${group_vars}
  # Kali Linux settings
  kali_package: "${KALI_PACKAGE_NAME}"

  # VNC settings
  vnc_username: "${VNC_USERNAME}"

  # Other variables
  username: "${USER_NAME}"
  default_dns: "$(hostname -I | awk '{print $1}'| tr '.' '-' | awk {'print $1 ".ip.linodeusercontent.com"'})"
EOF

  # Handle VNC enabled/disabled
  if [ "${VNC}" = "Yes" ]; then
    echo "vnc_enabled: true" >> ${group_vars}
  else
    echo "vnc_enabled: false" >> ${group_vars}
  fi

  # Handle disable root setting
  if [ "${DISABLE_ROOT}" = "Yes" ]; then
    echo "disable_root: true" >> ${group_vars}
  else
    echo "Leaving root login enabled"
  fi
}

function run {
  # Set debconf to automatically handle service restarts
  echo 'libc6:amd64 libraries/restart-without-asking boolean true' | debconf-set-selections
  echo 'libc6 libraries/restart-without-asking boolean true' | debconf-set-selections
  # install dependencies
  DEBIAN_FRONTEND=noninteractive apt-get update
  DEBIAN_FRONTEND=noninteractive apt-get install -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" \
    git \
    gnupg \
    python3 \
    python3-pip \
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
run
installation_complete
