#!/bin/bash

# enable logging
exec > >(tee /dev/ttyS0 /var/log/stackscript.log) 2>&1

# modes
DEBUG="NO"
if [ "${DEBUG}" == "NO" ]; then
  trap "cleanup $? $LINENO" EXIT
fi

if [ "${MODE}" == "staging" ]; then
  trap "provision_failed $? $LINENO" ERR
else
  set -e
fi

## Linode/SSH security settings
#<UDF name="user_name" label="The limited sudo user to be created for the Linode: *No Capital Letters or Special Characters*">
#<UDF name="disable_root" label="Disable root access over SSH?" oneOf="Yes,No" default="No">

## MySQL settings
#<UDF name="database" label="Install either MySQL-Server or MariaDB-Server" oneOf="mariadb,mysql" default="mariadb"

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
export MARKETPLACE_APP="apps/linode-marketplace-mysql"

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
        \"type\":\"${TYPE}\", \"region\":\"${REGION}\", \"env\":\"${ENV}\" }"
  
  exit $?
}

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
  # database install option
  database: ${DATABASE}
EOF

  if [ "$DISABLE_ROOT" = "Yes" ]; then
    echo "disable_root: yes" >> ${group_vars};
  else echo "Leaving root login enabled";
  fi

  if [[ -n ${DOMAIN} ]]; then
    echo "domain: ${DOMAIN}" >> ${group_vars};
  else
    echo "default_dns: $(hostname -I | awk '{print $1}'| tr '.' '-' | awk {'print $1 ".ip.linodeusercontent.com"'})" >> ${group_vars};
  fi

  if [[ -n ${SUBDOMAIN} ]]; then
    echo "subdomain: ${SUBDOMAIN}" >> ${group_vars};
  else echo "subdomain: www" >> ${group_vars};
  fi

  if [[ -n ${TOKEN_PASSWORD} ]]; then
    echo "token_password: ${TOKEN_PASSWORD}" >> ${group_vars};
  else echo "No API token entered";
  fi

  if [[ -n ${SOA_EMAIL_ADDRESS} ]]; then
    echo "soa_email_address: ${SOA_EMAIL_ADDRESS}" >> ${group_vars};
  fi

  # staging or production mode (ci)
  if [[ "${MODE}" == "staging" ]]; then
    echo "[info] running in staging mode..."
    echo "mode: ${MODE}" >> ${group_vars}
  else
    echo "[info] running in production mode..."
    echo "mode: production" >> ${group_vars}
  fi
}

function run {
  # install dependancies
  apt-get update
  apt-get install -y git python3 python3-pip

  # clone repo and set up ansible environment
  #git -C /tmp clone ${GIT_REPO}
  # for a single testing branch
  git -C /tmp clone -b ${BRANCH} ${GIT_REPO}

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