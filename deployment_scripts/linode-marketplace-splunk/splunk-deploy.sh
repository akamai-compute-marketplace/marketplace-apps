#!/bin/bash
set -e
trap "cleanup $? $LINENO" EXIT

##Linode/SSH security settings
#<UDF name="user_name" label="The limited sudo user to be created for the Linode: *All lowercase*">
#<UDF name="disable_root" label="Disable root access over SSH?" oneOf="Yes,No" default="No">

## Domain Settings
#<UDF name="token_password" label="Your Linode API token. This is needed to create your server's DNS records" default="">
#<UDF name="subdomain" label="Subdomain" example="The subdomain for the DNS record: www (Requires Domain)" default="">
#<UDF name="domain" label="Domain" example="The domain for the DNS record: example.com (Requires API token)" default="">

## Let's Encrypt Settings 
#<UDF name="soa_email_address" label="Admin Email for Let's Encrypt SSL certificate">

## Splunk Settings
#<UDF name="splunk_user" Label="Splunk Admin User">

## Akamai SIEM Settings
#<UDF name="sslheader" label="Akamai SIEM Settings" header="Yes" default="Yes">
#<UDF name="access_token_password" Label="Akamai Access Token" default="">
#<UDF name="client_secret_password" Label="Akamai Client Secret" default="">
#<UDF name="client_token_password" Label="Akamai Client Token" default="">
#<UDF name="hostname" Label="Akamai LUNA hostname" default="">
#<UDF name="security_config_id" Label="Configuration ID" default="">

# git repo
export GIT_REPO="https://github.com/akamai-compute-marketplace/marketplace-apps.git"
export WORK_DIR="/tmp/marketplace-apps" 
export MARKETPLACE_APP="apps/linode-marketplace-splunk"

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
  splunk_user: ${SPLUNK_USER}
  webserver_stack: standalone
EOF
  
  # START akamai SIEM settings

  if [[ -n ${ACCESS_TOKEN_PASSWORD} ]]; then
    echo "siem_access_token: ${ACCESS_TOKEN_PASSWORD}" >> ${group_vars}
  else 
    echo "Akamai access token not found"
  fi  

  if [[ -n ${CLIENT_SECRET_PASSWORD} ]]; then
    echo "siem_client_secret: ${CLIENT_SECRET_PASSWORD}" >> ${group_vars}
  else 
    echo "Akamai secret token not found"
  fi

  if [[ -n ${CLIENT_TOKEN_PASSWORD} ]]; then
    echo "siem_client_token: ${CLIENT_TOKEN_PASSWORD}" >> ${group_vars}
  else 
    echo "Akamai client token not found"
  fi  

  if [[ -n ${HOSTNAME} ]]; then
    echo "siem_hostname: ${HOSTNAME}" >> ${group_vars}
  else 
    echo "Akamai LUNA hostname not found"
  fi

  if [[ -n ${SECURITY_CONFIG_ID} ]]; then
    echo "security_config_id: ${SECURITY_CONFIG_ID}" >> ${group_vars}
  else 
    echo "Akamai configuration ID not found"
  fi 

# if vars are empty, that's okay - we don't configure the plugin. However if one of the variables
# is filled in, all must not be empty. If so, configuration will not work which will default to not
# installing the akamai-siem.

  if [[ -z "$ACCESS_TOKEN_PASSWORD" && -z "$CLIENT_SECRET_PASSWORD" && -z "$CLIENT_TOKEN_PASSWORD" \
    && -z "$HOSTNAME" && -z "$SECURITY_CONFIG_ID" ]]; then
    echo "Akamai SIEM not configured.."
    echo "install_akamai_siem: 'NO'" >> ${group_vars}
  else
    if [[ -n "$ACCESS_TOKEN_PASSWORD" && -n "$CLIENT_SECRET_PASSWORD" && -n "$CLIENT_TOKEN_PASSWORD" \
      && -n "$HOSTNAME" && -n "$SECURITY_CONFIG_ID" ]]; then
      echo "Configuring Akamai SIEM.."
      echo "install_akamai_siem: 'YES'" >> ${group_vars}
    else
      echo "[error] Akamai SIEM cannot be installed. We are missing one of the variables for configuration.."
      echo "install_akamai_siem: 'NO'" >> ${group_vars}
    fi
  fi 

  # END akamai SIEM settings

  if [[ -n ${USER_NAME} ]]; then
    echo "username: ${USER_NAME}" >> ${group_vars}
  else 
    echo "No username entered"
  fi

  if [ "$DISABLE_ROOT" = "Yes" ]; then
    echo "disable_root: yes" >> ${group_vars}
  else 
    echo "Leaving root login enabled"
  fi

  # vars
  
  if [[ -n ${SOA_EMAIL_ADDRESS} ]]; then
    echo "soa_email_address: ${SOA_EMAIL_ADDRESS}" >> ${group_vars}
  fi

  if [[ -n ${DOMAIN} ]]; then
    echo "domain: ${DOMAIN}" >> ${group_vars}
  else
    echo "default_dns: $(hostname -I | awk '{print $1}'| \
      tr '.' '-' | awk {'print $1 ".ip.linodeusercontent.com"'})" >> ${group_vars}
  fi

  if [[ -n ${SUBDOMAIN} ]]; then
    echo "subdomain: ${SUBDOMAIN}" >> ${group_vars}
  else 
    echo "subdomain: www" >> ${group_vars}
  fi
 
  if [[ -n ${TOKEN_PASSWORD} ]]; then
    echo "token_password: ${TOKEN_PASSWORD}" >> ${group_vars}
  else 
    echo "No API token entered"
  fi

}

function run {
  # install dependancies
  apt-get update
  apt-get install -y git python3 python3-pip

  # clone repo and set up ansible environment
  git -C /tmp clone ${GIT_REPO}
  # for a single testing branch
  #git -C /tmp clone -b ${BRANCH} ${GIT_REPO}

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