#!/bin/bash
set -e
DEBUG="NO"
if [ "${DEBUG}" == "NO" ]; then
  trap "cleanup $? $LINENO" EXIT
fi

##Linode/SSH security settings
#<UDF name="user_name" label="The limited sudo user to be created for the Linode: *All lowercase*">
#<UDF name="disable_root" label="Disable root access over SSH?" oneOf="Yes,No" default="No">

## Domain Settings
#<UDF name="token_password" label="Your Linode API token. This is needed to create your server's DNS records" default="">
#<UDF name="subdomain" label="Subdomain" example="The subdomain for the DNS record: www (Requires Domain)" default="">
#<UDF name="domain" label="Domain" example="The domain for the DNS record: example.com (Requires API token)" default="">

## Let's Encrypt Settings 
#<UDF name="soa_email_address" label="Admin Email for Let's Encrypt SSL certificate">

## Jenkins
#<UDF name="jenkins_version" label="Jenkins Version" oneOf="2.479" default="2.479" >

# git repo
export GIT_REPO="https://github.com/akamai-compute-marketplace/marketplace-apps.git"
export WORK_DIR="/tmp/marketplace-apps" 
export MARKETPLACE_APP="apps/linode-marketplace-jenkins"

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
  soa_email_address: ${SOA_EMAIL_ADDRESS}
  jenkins_version: ${JENKINS_VERSION}
  webserver_stack: standalone
EOF


  if [ "$DISABLE_ROOT" = "Yes" ]; then
    echo "disable_root: yes" >> ${group_vars}
  else 
    echo "Leaving root login enabled"
  fi

  # vars
  
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
