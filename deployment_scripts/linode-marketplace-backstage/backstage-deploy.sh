#!/bin/bash
set -e
DEBUG="NO"
if [ "${DEBUG}" == "NO" ]; then
  trap "cleanup $? $LINENO" EXIT
fi

## Linode/SSH security settings
#<UDF name="user_name" label="The limited sudo user to be created for the Linode: *No Capital Letters or Special Characters*">
#<UDF name="disable_root" label="Disable root access over SSH?" oneOf="Yes,No" default="No">

## Domain Settings
#<UDF name="token_password" label="Your Linode API token. This is needed to create your server's DNS records">
#<UDF name="subdomain" label="Subdomain" example="The subdomain for the DNS record: www (Requires Domain)">
#<UDF name="domain" label="Domain" example="The domain for the DNS record: example.com (Requires API token)">

## backstage setup
#<UDF name="soa_email_address" label="Email address (for the Let's Encrypt SSL certificate)" example="user@example.com">
#<UDF name="allowed_ips" label="IP addresses allowed to access the frontend" example="192.0.2.21, 198.51.100.17" default="">

#<UDF name="app_name" label="Backstage application name">
#<UDF name="github_oauth_client_id" label="Github Oauth Client ID">
#<UDF name="github_oauth_client_secret" label="Github Oauth Client Secret">
#<UDF name="github_username" label="Github Username">
#<UDF name="backstage_orgname" label="Backstage Organization Name">
#<UDF name="github_pat" label="Github Personal Access Token" default="">

# git repo
export GIT_REPO="https://github.com/akamai-compute-marketplace/marketplace-apps.git"
export WORK_DIR="/tmp/marketplace-apps" 
export MARKETPLACE_APP="apps/linode-marketplace-backstage"

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
  webserver_stack: standalone
EOF

  if [ "$DISABLE_ROOT" = "Yes" ]; then
    echo "disable_root: yes" >> ${group_vars}
  else echo "Leaving root login enabled";
  fi

  if [[ -n ${DOMAIN} ]]; then
    echo "domain: ${DOMAIN}" >> ${group_vars}
  else
    echo "default_dns: $(hostname -I | awk '{print $1}'| tr '.' '-' | awk {'print $1 ".ip.linodeusercontent.com"'})" >> ${group_vars}
  fi

  if [[ -n ${SUBDOMAIN} ]]; then
    echo "subdomain: ${SUBDOMAIN}" >> ${group_vars}
  else echo "subdomain: www" >> ${group_vars}
  fi

  if [[ -n ${TOKEN_PASSWORD} ]]; then
    echo "token_password: ${TOKEN_PASSWORD}" >> ${group_vars}
  else echo "No API token entered";
  fi

  # backstage vars
  if [[ -n ${SOA_EMAIL_ADDRESS} ]]; then
    echo "soa_email_address: ${SOA_EMAIL_ADDRESS}" >> ${group_vars}
  fi

  if [[ -z ${ALLOWED_IPS} ]]; then
    echo "[info] No IP address provided for whitelisting"
  else
    echo "allowed_ips: ${ALLOWED_IPS}" >> ${group_vars}
  fi

  if [[ -n ${APP_NAME} ]]; then
    echo "app_name: ${APP_NAME}" >> ${group_vars}
  fi

  if [[ -n ${GITHUB_OAUTH_CLIENT_ID} ]]; then
    echo "github_oauth_client_id: ${GITHUB_OAUTH_CLIENT_ID}" >> ${group_vars}
  fi

  if [[ -n ${GITHUB_OAUTH_CLIENT_SECRET} ]]; then
    echo "github_oauth_client_secret: ${GITHUB_CLIENT_SECRET}" >> ${group_vars}
  fi

  if [[ -n ${GITHUB_USERNAME} ]]; then
    echo "github_username: ${GITHUB_USERNAME}" >> ${group_vars}
  fi

  if [[ -n ${BACKSTAGE_ORGNAME} ]]; then
    echo "backstage_orgname: '${BACKSTAGE_ORGNAME}'" >> ${group_vars}
  fi

  if [[ -n ${GITHUB_PAT} ]]; then
    echo "github_pat: ${GITHUB_PAT}" >> ${group_vars}
  fi  
}

function run {
  # install dependancies
  apt-get update
  apt-get install -y git python3 python3-pip  libpq-dev

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