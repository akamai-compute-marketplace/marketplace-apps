#!/bin/bash
set -e
trap "cleanup $? $LINENO" EXIT

##Linode/SSH security settings
#<UDF name="user_name" label="The limited sudo user to be created for the Linode" default="">
#<UDF name="password" label="The password for the limited sudo user" example="an0th3r_s3cure_p4ssw0rd" default="">
#<UDF name="disable_root" label="Disable root access over SSH?" oneOf="Yes,No" default="No">
#<UDF name="pubkey" label="The SSH Public Key that will be used to access the Linode (Recommended)" default="">

## Domain Settings
#<UDF name="token_password" label="Your Linode API token. This is needed to create your server's DNS records" default="">
#<UDF name="subdomain" label="Subdomain" example="The subdomain for the DNS record: www (Requires Domain)" default="">
#<UDF name="domain" label="Domain" example="The domain for the DNS record: example.com (Requires API token)" default="">

## nats Settings 
# <UDF name="name" label="Name" default="Test" />
# <UDF name="version" label="Version" oneOf="2.10.1,2.10.0,2.9.22,2.9.21,2.9.20" default="2.10.1" />
# <UDF name="system_user_password" label="System User Password" />
# <UDF name="example_user_password" label="Example User Password" />
#<UDF name="soa_email_address" label="Email address (for the Let's Encrypt SSL certificate)" example="user@domain.tld">
# <UDF name="nats_port" label="Nats Server Port" default="4222" />
# <UDF name="monitor_port" label="Nats Monitor Port" default="8222" />
# <UDF name="mqtt_port" label="Nats MQTT Port" default="1883" />


# git repo
export GIT_REPO="https://github.com/jcotoBan/marketplace-apps.git"
export WORK_DIR="/tmp/marketplace-apps" 
export MARKETPLACE_APP="apps/linode-marketplace-nats-single-node"

# enable logging
exec > >(tee /dev/ttyS0 /var/log/stackscript.log) 2>&1

function cleanup {
  if [ -d "${WORK_DIR}" ]; then
    rm -rf ${WORK_DIR}
  fi

}

function udf {
  local group_vars="${WORK_DIR}/${MARKETPLACE_APP}/group_vars/linode/vars"
  echo "webserver_stack: lemp" >> ${group_vars};
  
  if [[ -n ${USER_NAME} ]]; then
    echo "username: ${USER_NAME}" >> ${group_vars};
  else echo "No username entered";
  fi

  if [ "$DISABLE_ROOT" = "Yes" ]; then
    echo "disable_root: yes" >> ${group_vars};
  else echo "Leaving root login enabled";
  fi

  if [[ -n ${PASSWORD} ]]; then
    echo "password: ${PASSWORD}" >> ${group_vars};
  else echo "No password entered";
  fi

  if [[ -n ${PUBKEY} ]]; then
    echo "pubkey: ${PUBKEY}" >> ${group_vars};
  else echo "No pubkey entered";
  fi

  if [[ -n ${SOA_EMAIL_ADDRESS} ]]; then
    echo "soa_email_address: ${SOA_EMAIL_ADDRESS}" >> ${group_vars};
  fi

  if [[ -n ${DOMAIN} ]]; then
    echo "domain: ${DOMAIN}" >> ${group_vars};
  else
    echo "default_dns: $(hostname -I | awk '{print $1}'| tr '.' '-' | awk {'print $1 ".ip.linodeusercontent.com"'})" >> ${group_vars};
  fi


  if [[ -n ${SUBDOMAIN} ]]; then
    echo "subdomain: ${SUBDOMAIN}" >> ${group_vars};
  else 
    echo "subdomain: www" >> ${group_vars};
  fi


  #nats vars
  
  if [[ -n ${NAME} ]]; then
    echo "name: ${NAME}" >> ${group_vars};
  fi

  if [[ -n ${VERSION} ]]; then
    echo "version: ${VERSION}" >> ${group_vars};
  fi

  if [[ -n ${SYSTEM_USER_PASSWORD} ]]; then
    echo "system_user_password: ${SYSTEM_USER_PASSWORD}" >> ${group_vars};
  fi

  if [[ -n ${EXAMPLE_USER_PASSWORD} ]]; then
    echo "example_user_password: ${EXAMPLE_USER_PASSWORD}" >> ${group_vars};
  fi

  if [[ -n ${NATS_PORT} ]]; then
    echo "nats_port: ${NATS_PORT}" >> ${group_vars};
  fi

  if [[ -n ${MONITOR_PORT} ]]; then
    echo "monitor_port: ${MONITOR_PORT}" >> ${group_vars};
  fi

  if [[ -n ${MQTT_PORT} ]]; then
    echo "mqtt_port: ${MQTT_PORT}" >> ${group_vars};
  fi

}

function run {
  # install dependancies
  apt-get update
  apt-get install -y git python3 python3-pip

  # clone repo and set up ansible environment
  git -C /tmp clone -b nats-single-node ${GIT_REPO} #to test, change accord.
  # for a single testing branch
  # git -C /tmp clone --single-branch --branch ${BRANCH} ${GIT_REPO}

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
  for playbook in site.yml; do ansible-playbook -vvvv $playbook; done
  
}

function installation_complete {
  echo "Installation Complete"
}
# main
run && installation_complete
cleanup
