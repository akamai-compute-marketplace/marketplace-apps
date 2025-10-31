#!/bin/bash

# enable logging
exec > >(tee /dev/ttyS0 /var/log/stackscript.log) 2>&1

# BEGIN CI-MODE
# modes
#DEBUG="NO"
if [[ -n ${DEBUG} ]]; then
  if [ "${DEBUG}" == "NO" ]; then
    trap "cleanup $? $LINENO" EXIT
  fi
else
  trap "cleanup $? $LINENO" EXIT
fi
# END CI-MODE

## Linode/SSH security settings
#<UDF name="user_name" label="The limited sudo user to be created for the Linode: *No Capital Letters or Special Characters*">
#<UDF name="disable_root" label="Disable root access over SSH?" oneOf="Yes,No" default="No">

## Domain Settings
#<UDF name="domain" label="Domain name for your Prometheus & Grafana instance. (Requires API Token)" default="">
#<UDF name="subdomain" label="Subdomain" example="The subdomain for the DNS record: www (Requires Domain)" default="www">
#<UDF name="token_password" label="Your Linode API token" default="">
#<UDF name="soa_email_address" label="Email address (for the Let's Encrypt SSL certificate)" example="user@domain.tld">

## Akamai Datasource
# <UDF name="akamai_client_secret" label="Akamai client_secret" example="Example: abcdEcSnaAt123FNkBxy456z25qx9Yp5CPUxlEfQeTDkfh4QA=I" default="" />
# <UDF name="akamai_host" label="Akamai host" example="Example:  akab-lmn789n2k53w7qrs10cxy-nfkxaa4lfk3kd6ym.luna.akamaiapis.net" default="" />
# <UDF name="akamai_access_token" label="Akamai access_token" example="Example: akab-zyx987xa6osbli4k-e7jf5ikib5jknes3" default="" />
# <UDF name="akamai_client_token" label="Akamai client_token" example="Example: akab-nomoflavjuc4422-fa2xznerxrm3teg7" default="" />

## Loki Datasource
# <UDF name="install_loki" label="Install Loki as data source?" oneOf="Yes,No" default="No" />

# BEGIN CI-ADDONS
## Addons
#<UDF name="add_ons" label="Optional data exporter Add-ons for your deployment" manyOf="node_exporter,mysqld_exporter,newrelic,none" default="none">
# END CI-ADDONS

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
export MARKETPLACE_APP="apps/linode-marketplace-prometheus-grafana"

# BEGIN CI-PROVISION-FUNC
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
# END CI-PROVISION-FUNC

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
  prometheus_exporter: [node_exporter]
  webserver_stack: lemp
  # BEGIN CI-UDF-ADDONS
  # addons
  add_ons: [${ADD_ONS}]
  # END CI-UDF-ADDONS   
EOF

  if [ "$DISABLE_ROOT" = "Yes" ]; then
    echo "disable_root: yes" >> ${group_vars}
  else echo "Leaving root login enabled"
  fi

  # domain vars
  if [[ -n ${SOA_EMAIL_ADDRESS} ]]; then
    echo "soa_email_address: ${SOA_EMAIL_ADDRESS}" >> ${group_vars}
  fi

  if [[ -n ${DOMAIN} ]]; then
    echo "domain: ${DOMAIN}" >> ${group_vars}
  else
    echo "default_dns: $(hostname -I | awk '{print $1}'| tr '.' '-' | awk {'print $1 ".ip.linodeusercontent.com"'})" >> ${group_vars}
  fi

  if [[ -n ${SUBDOMAIN} ]]; then
    echo "subdomain: ${SUBDOMAIN}" >> ${group_vars}
  else 
    echo "subdomain: www" >> ${group_vars}
  fi

  if [[ -n ${TOKEN_PASSWORD} ]]; then
    echo "token_password: ${TOKEN_PASSWORD}" >> ${group_vars}
  else echo "No API token entered"
  fi

  if [[ "$INSTALL_LOKI" == "Yes" ]]; then
    echo "install_loki: true" >> ${group_vars}
  else
    echo "install_loki: false" >> ${group_vars}
  fi

  # akamai datasource
  if [[ -n ${AKAMAI_CLIENT_SECRET} ]] && [[ -n ${AKAMAI_HOST} ]] && [[ -n ${AKAMAI_ACCESS_TOKEN} ]] && [[ -n ${AKAMAI_CLIENT_TOKEN} ]]; then
    echo "akamai_datasource: True" >> ${group_vars}
    echo "akamai_client_secret: ${AKAMAI_CLIENT_SECRET}" >> ${group_vars}
    echo "akamai_host: ${AKAMAI_HOST}"  >> ${group_vars}
    echo "akamai_access_token: ${AKAMAI_ACCESS_TOKEN}"  >> ${group_vars}
    echo "akamai_client_token: ${AKAMAI_CLIENT_TOKEN}"  >> ${group_vars}
  else
    echo "[info] Missing variable in the Akamai datasource. Not configuring"
    echo "akamai_datasource: False" >> ${group_vars}
  fi

  # staging or production mode (ci)
  # BEGIN CI-UDF-CI-MODE
  # staging or production mode (ci)
  if [[ "${MODE}" == "staging" ]]; then
    echo "[info] running in staging mode..."
    echo "mode: ${MODE}" >> ${group_vars}
  else
    echo "[info] running in production mode..."
    echo "mode: production" >> ${group_vars}
  fi
# END CI-UDF-CI-MODE  
}

function run {
  # install dependancies
  apt-get update
  apt-get install -y git python3 python3-pip

  # clone repo and set up ansible environment
  git -C /tmp clone -b ${BRANCH} ${GIT_REPO}

  # set up python virtual environment
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