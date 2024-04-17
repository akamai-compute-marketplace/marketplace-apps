#!/bin/bash
set -e
trap "cleanup $? $LINENO" EXIT

##Linode/SSH security settings
#<UDF name="user_name" label="The limited sudo user to be created for the Linode: *No Capital Letters or Special Characters*">
#<UDF name="disable_root" label="Disable root access over SSH?" oneOf="Yes,No" default="No">
#<UDF name="django_superuser_username" label="Django Admin Username" example="myadmin">
#<UDF name="django_superuser_email" label="Django Admin Email Address" example="user@domain.tld">
#<UDF name="django_superuser_password" label="Django Admin Password" fieldType="password" example="aComplexP@ssword">

## Domain Settings
#<UDF name="token_password" label="Your Linode API token. This is needed to create your server's DNS records" default="">
#<UDF name="subdomain" label="Subdomain" example="The subdomain for the DNS record: www (Requires Domain)" default="">
#<UDF name="domain" label="Domain" example="The domain for the DNS record: example.com (Requires API token)" default="">

# git repo
export GIT_REPO="https://github.com/akamai-compute-marketplace/marketplace-apps.git"
export WORK_DIR="/tmp/marketplace-apps" 
export MARKETPLACE_APP="apps/linode-marketplace-openlitespeed-django"
export VHDOCROOT="/usr/local/lsws/Example/html"
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
EOF
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
  python3 -m virtualenv ${VHDOCROOT}/
  source ${VHDOCROOT}/bin/activate
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