#!/bin/bash

set -e
trap "cleanup $? $LINENO" EXIT

## Linode/SSH Security Settings
#<UDF name="user_name" label="The limited sudo user to be created for the Linode" default="">
#<UDF name="password" label="The password for the limited sudo user" example="an0th3r_s3cure_p4ssw0rd" default="">
#<UDF name="disable_root" label="Disable root access over SSH?" oneOf="Yes,No" default="No">
#<UDF name="pubkey" label="The SSH Public Key that will be used to access the Linode (Recommended)" default="">

## Domain Settings
#<UDF name="token_password" label="Your Linode API token. This is needed to create your Linode's DNS records" default="">
#<UDF name="subdomain" label="Subdomain" example="The subdomain for the DNS record. `www` will be entered if no subdomain is supplied (Requires Domain)" default="">
#<UDF name="domain" label="Domain" example="The domain for the DNS record: example.com (Requires API token)" default="">
#<UDF name="soa_email_address" label="Email address for SOA record" default=””>

# git repo
#export GIT_REPO="https://github.com/akamai-compute-marketplace/marketplace-apps.git"

#test git repo
export GIT_REPO="https://github.com/akamai-compute-marketplace/marketplace-apps.git"
export BRANCH="develop"

export WORK_DIR="/tmp/marketplace-apps"
export MARKETPLACE_APP="apps/linode-marketplace-mc-live-encoder-demo"

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

  # deployment vars
  soa_email_address: ${SOA_EMAIL_ADDRESS}
EOF

  if [[ -n ${USER_NAME} ]]; then
    echo "username: ${USER_NAME}" >> ${group_vars};
  else echo "No username entered";
  fi

  if [[ -n ${PASSWORD} ]]; then
    echo "password: ${PASSWORD}" >> ${group_vars};
  else echo "No password entered";
  fi

  if [[ -n ${PUBKEY} ]]; then
    echo "pubkey: ${PUBKEY}" >> ${group_vars};
  else echo "No pubkey entered";
  fi

  if [[ -n ${TOKEN_PASSWORD} ]]; then
    echo "token_password: ${TOKEN_PASSWORD}" >> ${group_vars};
  else echo "No API token entered";
  fi

  if [[ -n ${DOMAIN} ]]; then
    echo "domain: ${DOMAIN}" >> ${group_vars};
  #else echo "No domain entered";
  else echo "default_dns: $(dnsdomainname -A | awk '{print $1}')" >> ${group_vars};
  fi

  if [[ -n ${SUBDOMAIN} ]]; then
    echo "subdomain: ${SUBDOMAIN}" >> ${group_vars};
  else echo "subdomain: www" >> ${group_vars};
  fi
}

function run {
  # install dependancies
  yum install dnf -y
  dnf update -y
  dnf upgrade -y
  dnf install https://packages.endpointdev.com/rhel/7/os/x86_64/endpoint-repo.x86_64.rpm -y
  dnf install -y git python3 python3-pip

  dnf makecache
  dnf install epel-release -y
  dnf makecache
  dnf install ansible -y

  # clone repo and set up ansible environment
  # git -C /tmp clone ${GIT_REPO}
  # for a single testing branch
  git -C /tmp clone --single-branch --branch ${BRANCH} ${GIT_REPO}

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
  for playbook in provision.yml site.yml; do ansible-playbook -vvvv $playbook; done
}

function installation_complete {
  # dumping credentials  
  echo -e "username=admin\npassword=admin" > /root/.linode_credentials.txt
  cat << EOF
#########################
# INSTALLATION COMPLETE #
############################################
# * Hugs are worth more than handshakes *  #
############################################
EOF
}
# main
run && installation_complete
cleanup