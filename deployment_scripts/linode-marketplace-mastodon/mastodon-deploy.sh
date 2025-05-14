#!/bin/bash
set -e
trap "cleanup $? $LINENO" EXIT

## Linode/SSH Security Settings
#<UDF name="user_name" label="The limited sudo user to be created for the Linode: *No Capital Letters or Special Characters*">
#<UDF name="disable_root" label="Disable root access over SSH?" oneOf="Yes,No" default="No">

## Mastodon Settings
#<UDF name="domain" label="Domain name for your Mastodon instance." example="domain.tld" />
#<UDF name="subdomain" label="Subdomain" example="The subdomain for the DNS record: www (Requires Domain)" default="www">
#<UDF name="token_password" label="Your Linode API token" />
#<UDF name="soa_email_address" label="Email address (for the Let's Encrypt SSL certificate)" example="user@domain.tld" />
#<UDF name="owner_username" label="Username for Mastodon Owner" example="" />
#<UDF name="owner_email" label="Email address for Mastodon Owner" example="user@domain.tld" />
#<UDF name="single_user_mode" label="Do you want to start Mastodon in single-user mode?" oneOf="Yes,No" />

# git repo
export GIT_REPO="https://github.com/akamai-compute-marketplace/marketplace-apps.git"
export WORK_DIR="/tmp/marketplace-apps" 
export MARKETPLACE_APP="apps/linode-marketplace-mastodon"

# enable logging
exec > >(tee /dev/ttyS0 /var/log/stackscript.log) 2>&1

function cleanup {
  if [ -d "${WORK_DIR}" ]; then
    rm -rf ${WORK_DIR}
  fi
}

function udf {
  
  local group_vars="${WORK_DIR}/${MARKETPLACE_APP}/group_vars/linode/vars"
  
   # write udf vars
  cat <<END > ${group_vars}
# sudo username
username: ${USER_NAME}
webserver_stack: lemp
domain: ${DOMAIN}
subdomain: ${SUBDOMAIN}
soa_email_address: ${SOA_EMAIL_ADDRESS}
owner_username: ${OWNER_USERNAME}
owner_email: ${OWNER_EMAIL}
single_user_mode: ${SINGLE_USER_MODE}
token_password: ${TOKEN_PASSWORD}
END

  if [ "$DISABLE_ROOT" = "Yes" ]; then
    echo "disable_root: yes" >> ${group_vars};
  else echo "Leaving root login enabled";
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
  ansible-playbook -v provision.yml && ansible-playbook -v site.yml
  
}

function installation_complete {
  echo "Installation Complete"
}
# main
run && installation_complete
cleanup
