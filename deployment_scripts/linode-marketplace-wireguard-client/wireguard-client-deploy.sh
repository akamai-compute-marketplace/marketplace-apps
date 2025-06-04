#!/bin/bash

# enable logging
exec > >(tee /dev/ttyS0 /var/log/stackscript.log) 2>&1

# modes
#DEBUG="NO"
if [[ -n ${DEBUG} ]]; then
  if [ "${DEBUG}" == "NO" ]; then
    trap "cleanup $? $LINENO" EXIT
  fi
else
  trap "cleanup $? $LINENO" EXIT
fi

if [ "${MODE}" == "staging" ]; then
  trap "provision_failed $? $LINENO" ERR
else
  set -e
fi

## Linode/SSH security settings
#<UDF name="user_name" label="The limited sudo user to be created for the Linode: *No Capital Letters or Special Characters*">
#<UDF name="disable_root" label="Disable root access over SSH?" oneOf="Yes,No" default="No">

## WireGuard Settings
#<UDF name="wireguard_server_public_key" label="WireGuard Server Public Key (Base64)" example="5+m82uxMXQchGKbTb3lpQbxxG9g+GXz1vjFC6Pa8zi8=" />
#<UDF name="wireguard_server_endpoint" label="WireGuard Server Endpoint (IP:Port)" example="170.187.144.181:51820" />
#<UDF name="wireguard_client_tunnel_ip" label="WireGuard Client Tunnel IP (with /32)" example="10.0.0.2/32" default="10.0.0.2/32" />
#<UDF name="wireguard_allowed_ips" label="Allowed IPs (split tunnel)" example="10.0.0.1/32" default="10.0.0.1/32" />
#<UDF name="wireguard_persistent_keepalive" label="Persistent Keepalive (seconds)" example="25" default="25" />
#<UDF name="wireguard_mtu" label="WireGuard MTU (optional)" example="1420" default="1420" />
#<UDF name="wireguard_dns" label="DNS Servers (optional, comma-separated)" example="1.1.1.1,8.8.8.8" default="" />
#<UDF name="wireguard_use_preshared_key" label="Use Pre-shared Key?" oneOf="Yes,No" default="No" />

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
export MARKETPLACE_APP="apps/linode-marketplace-wireguard-client"

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
  wireguard_server_public_key: "${WIREGUARD_SERVER_PUBLIC_KEY}"
  wireguard_server_endpoint: "${WIREGUARD_SERVER_ENDPOINT}"
  wireguard_client_tunnel_ip: "${WIREGUARD_CLIENT_TUNNEL_IP}"
  wireguard_allowed_ips: "${WIREGUARD_ALLOWED_IPS}"
  wireguard_persistent_keepalive: "${WIREGUARD_PERSISTENT_KEEPALIVE}"
  wireguard_mtu: "${WIREGUARD_MTU}"
  wireguard_dns: "${WIREGUARD_DNS}"
  wireguard_use_preshared_key: "${WIREGUARD_USE_PRESHARED_KEY}"
EOF

  if [ "$DISABLE_ROOT" = "Yes" ]; then
    echo "disable_root: yes" >> ${group_vars};
  else echo "Leaving root login enabled";
  fi

  if [[ -n ${DOMAIN} ]]; then
    echo "domain: ${DOMAIN}" >> ${group_vars};
  else
    echo "default_dns: $(hostname -I | awk '{print $1}'| tr '.' '-' | awk {'print $1 ".ip.linodeusercontent.com"'})" >> ${group_vars};
  fi

  if [[ -n ${SUBDOMAIN} ]]; then
    echo "subdomain: ${SUBDOMAIN}" >> ${group_vars};
  else echo "subdomain: www" >> ${group_vars};
  fi

  if [[ -n ${TOKEN_PASSWORD} ]]; then
    echo "token_password: ${TOKEN_PASSWORD}" >> ${group_vars};
  else echo "No API token entered";
  fi

  if [[ -n ${SOA_EMAIL_ADDRESS} ]]; then
    echo "soa_email_address: ${SOA_EMAIL_ADDRESS}" >> ${group_vars};
  fi

  # staging or production mode (ci)
  if [[ "${MODE}" == "staging" ]]; then
    echo "[info] running in staging mode..."
    echo "mode: ${MODE}" >> ${group_vars}
  else
    echo "[info] running in production mode..."
    echo "mode: production" >> ${group_vars}
  fi  
}

function run {
  # install dependencies
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
