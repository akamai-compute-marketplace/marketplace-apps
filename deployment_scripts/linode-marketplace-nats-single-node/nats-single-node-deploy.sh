#!/bin/bash
set -e
trap "cleanup $? $LINENO" EXIT

##Linode/SSH security settings
#<UDF name="user_name" label="The limited sudo user to be created for the Linode: *No Capital Letters or Special Characters*">
#<UDF name="disable_root" label="Disable root access over SSH?" oneOf="Yes,No" default="No">

## Domain Settings
#<UDF name="token_password" label="Your Linode API token. This is needed to create your server's DNS records" default="">
#<UDF name="subdomain" label="Subdomain" example="The subdomain for the DNS record: www (Requires Domain)" default="">
#<UDF name="domain" label="Domain" example="The domain for the DNS record: example.com (Requires API token)" default="">

## nats Settings 
# <UDF name="name" label="NATS Server Name" default="Test" />
# <UDF name="version" label="Version" oneOf="2.10.1,2.10.0,2.9.22,2.9.21,2.9.20" default="2.10.1" />s
#<UDF name="soa_email_address" label="Email address (for the Let's Encrypt SSL certificate)" example="user@domain.tld">
# <UDF name="nats_port" label="NATS Server Port" default="4222" />
# <UDF name="websocket_port" label="NATS Websocket Port" default="8888" />
# <UDF name="mqtt_port" label="NATS MQTT Port" default="1883" />


# git repo
export GIT_REPO="https://github.com/akamai-compute-marketplace/marketplace-apps.git"
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

sed 's/  //g' <<EOF > ${group_vars}
  # sudo username
  username: ${USER_NAME}
  webserver_stack: lemp
EOF

  if [ "$DISABLE_ROOT" = "Yes" ]; then
    echo "disable_root: yes" >> ${group_vars};
  else echo "Leaving root login enabled";
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

  if [[ -n ${NATS_PORT} ]]; then
    echo "nats_port: ${NATS_PORT}" >> ${group_vars};
  fi

  if [[ -n ${WEBSOCKET_PORT} ]]; then
    echo "websocket_port: ${WEBSOCKET_PORT}" >> ${group_vars};
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
