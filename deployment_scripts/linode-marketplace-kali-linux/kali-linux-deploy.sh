#!/bin/bash
set -e
if [ "${DEBUG}" == "NO" ]; then
  trap "cleanup $? $LINENO" EXIT
fi

## Kali
#<UDF name="everything" label="Would you like to Install the Kali Everything Package?" oneOf="Yes,No" default="Yes">
#<UDF name="headless" label="Would you like to Install the Kali Headless Package?" oneOf="Yes,No" default="No">
#<UDF name="vnc" label="Would you like to setup VNC to access Kali XFCE Desktop" oneOf="Yes,No" default="Yes">
#<UDF name="vnc_username" label="The VNC user to be created for the Linode. The username accepts only lowercase letters, numbers, dashes (-) and underscores (_)">
#<UDF name="vnc_password" label="The password for the limited VNC user">

## Linode/SSH Security Settings
#<UDF name="user_name" label="The limited sudo user to be created for the Linode: *All lowercase*">
#<UDF name="disable_root" label="Disable root access over SSH?" oneOf="Yes,No" default="No">

## Domain Settings
#<UDF name="token_password" label="Your Linode API token. This is required for creating DNS records." default="">
#<UDF name="subdomain" label="The subdomain for the Linode's DNS record (Requires API token)" default="">
#<UDF name="domain" label="The domain for the Linode's DNS record (Requires API token)" default="">
#<UDF name="soa_email_address" label="Email address for SOA records (Requires API token)" default="">


# git repo
export GIT_REPO="https://github.com/akamai-compute-marketplace/marketplace-apps.git"
export WORK_DIR="/tmp/marketplace-apps" 
export MARKETPLACE_APP="apps/linode-marketplace-kali-linux"

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
  # Kali Linux settings
  kali_package: "{{ 'kali-linux-everything' if '${EVERYTHING}' == 'Yes' else 'kali-linux-headless' if '${HEADLESS}' == 'Yes' else '' }}"

  # VNC settings
  vnc_enabled: "{{ '${VNC}' == 'Yes' }}"
  vnc_username: "${VNC_USERNAME}"
  vnc_password: "${VNC_PASSWORD}"

  # Other variables
  username: "${USER_NAME}"
  disable_root: "{{ '${DISABLE_ROOT}' == 'Yes' }}"
  token_password: "${TOKEN_PASSWORD}"
  subdomain: "${SUBDOMAIN}"
  soa_email_address: "${SOA_EMAIL_ADDRESS}"
EOF

  if [[ -n ${DOMAIN} ]]; then
    echo "domain: ${DOMAIN}" >> ${group_vars};
  else
    echo "default_dns: $(hostname -I | awk '{print $1}'| tr '.' '-' | awk {'print $1 ".ip.linodeusercontent.com"'})" >> ${group_vars};
  fi

  if [[ -z ${SUBDOMAIN} ]]; then
    echo "subdomain: www" >> ${group_vars};
  fi

  if [[ -n ${TOKEN_PASSWORD} ]]; then
    echo "token_password: ${TOKEN_PASSWORD}" >> ${group_vars};
  else echo "No API token entered";
  fi
}

function run {
  # Set debconf to automatically handle service restarts
  # echo 'libc6:amd64 libraries/restart-without-asking boolean true' | debconf-set-selections
  # echo 'libc6 libraries/restart-without-asking boolean true' | debconf-set-selections
  # install dependencies
  # DEBIAN_FRONTEND=noninteractive apt-get update
  # DEBIAN_FRONTEND=noninteractive apt-get install -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" \
  #   git \
  #   python3 \
  #   python3-pip \
  #   python3-venv \
  #   python3-full \
  #   ansible
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
