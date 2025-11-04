#!/bin/bash

# enable logging
exec > >(tee /dev/ttyS0 /var/log/stackscript.log) 2>&1

# modes
# DEBUG="NO"
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

## Domain Settings
#<UDF name="token_password" label="Your Linode API token. This is needed to create your server's DNS records" default="">
#<UDF name="subdomain" label="Subdomain" example="The subdomain for the DNS record: www (Requires Domain)" default="">
#<UDF name="domain" label="Domain" example="The domain for the DNS record: example.com (Requires API token)" default="">
#<UDF name="soa_email_address" label="Email address (for the Let's Encrypt SSL certificate)" example="user@domain.tld">

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
export MARKETPLACE_APP="apps/linode-marketplace-weaviate"

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
EOF

  if [ "$DISABLE_ROOT" = "Yes" ]; then
    echo "disable_root: yes" >> ${group_vars};
  else echo "Leaving root login enabled";
  fi

  if [[ -n ${SUBDOMAIN} ]]; then
    echo "subdomain: ${SUBDOMAIN}" >> ${group_vars};
  fi

  if [[ -n ${DOMAIN} ]]; then
    echo "domain: ${DOMAIN}" >> ${group_vars};
  else
    echo "default_dns: $(hostname -I | awk '{print $1}'| tr '.' '-' | awk {'print $1 ".ip.linodeusercontent.com"'})" >> ${group_vars};
  fi

  if [[ -n ${TOKEN_PASSWORD} ]]; then
    echo "token_password: ${TOKEN_PASSWORD}" >> ${group_vars};
  else echo "No API token entered";
  fi

  if [[ -n ${SOA_EMAIL_ADDRESS} ]]; then
    echo "soa_email_address: ${SOA_EMAIL_ADDRESS}" >> ${group_vars};
  else echo "No SOA email entered";
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
  local resume_marker="/root/.weaviate-deploy-resume"
  local udf_backup="/root/.weaviate-udf-backup"

  # check if this is post-reboot continuation
  if [ -f "$resume_marker" ]; then
    echo "[info] === Resuming deployment after reboot for NVIDIA driver kernel ==="
    rm -f "$resume_marker"

    # restore UDF variables from backup
    if [ -f "$udf_backup" ]; then
      source "$udf_backup"
      echo "[info] Restored UDF variables"
    fi

    # re-clone repo (in case /tmp was cleared during reboot)
    rm -rf ${WORK_DIR}
    git -C /tmp clone -b ${BRANCH} ${GIT_REPO}

    cd ${WORK_DIR}/${MARKETPLACE_APP}

    # recreate venv
    apt install -y python3-venv
    python3 -m venv env
    source env/bin/activate
    pip install pip --upgrade
    pip install -r requirements.txt
    ansible-galaxy install -r collections.yml

    # regenerate group_vars from backed up UDF values
    udf

    # run playbooks
    ansible-playbook -v provision.yml && ansible-playbook -v site.yml

    # cleanup resume service
    systemctl disable weaviate-deploy-resume.service 2>/dev/null || true
    rm -f /etc/systemd/system/weaviate-deploy-resume.service
    rm -f "$udf_backup"
    systemctl daemon-reload

    return 0
  fi

  # === FIRST RUN: Initial setup ===
  # install dependencies
  apt-get update
  apt-get install -y git python3 python3-pip python3-venv

  # backup UDF variables before potential reboot
  cat > "$udf_backup" <<EOF
export USER_NAME="${USER_NAME}"
export DISABLE_ROOT="${DISABLE_ROOT}"
export TOKEN_PASSWORD="${TOKEN_PASSWORD}"
export SUBDOMAIN="${SUBDOMAIN}"
export DOMAIN="${DOMAIN}"
export SOA_EMAIL_ADDRESS="${SOA_EMAIL_ADDRESS}"
export MODE="${MODE}"
export GH_USER="${GH_USER}"
export BRANCH="${BRANCH}"
export GIT_REPO="${GIT_REPO}"
export WORK_DIR="${WORK_DIR}"
export MARKETPLACE_APP="${MARKETPLACE_APP}"
EOF

  # upgrade system packages BEFORE ansible setup (GPU instances need matching nvidia modules)
  echo "[info] Upgrading system packages for NVIDIA driver compatibility..."
  DEBIAN_FRONTEND=noninteractive apt-get upgrade -y

  # check if reboot is required BEFORE doing any ansible work
  if [ -f /var/run/reboot-required ]; then
    echo "[info] Kernel upgraded - reboot required for NVIDIA drivers"
    echo "[info] Configuring post-reboot auto-resume..."

    # create systemd oneshot service to resume after reboot
    cat > /etc/systemd/system/weaviate-deploy-resume.service <<EOF
[Unit]
Description=Resume Weaviate Deployment After Kernel Upgrade
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/bin/bash -c "exec > >(tee -a /dev/ttyS0 /var/log/stackscript.log) 2>&1; source /root/.weaviate-udf-backup; cd /tmp && curl -s https://raw.githubusercontent.com/${GH_USER}/marketplace-apps/${BRANCH}/deployment_scripts/linode-marketplace-weaviate/weaviate-deploy.sh | bash"
StandardOutput=journal+console
StandardError=journal+console

[Install]
WantedBy=multi-user.target
EOF

    # create resume marker
    touch "$resume_marker"

    systemctl daemon-reload
    systemctl enable weaviate-deploy-resume.service

    echo "[info] ============================================"
    echo "[info] Rebooting to load new kernel with NVIDIA drivers..."
    echo "[info] Deployment will automatically resume after reboot"
    echo "[info] Check /var/log/stackscript.log for progress"
    echo "[info] ============================================"
    sleep 5
    reboot
    exit 0
  fi

  # no reboot needed - clone repo and continue normally
  echo "[info] No kernel upgrade needed, continuing with deployment..."
  git -C /tmp clone -b ${BRANCH} ${GIT_REPO}

  cd ${WORK_DIR}/${MARKETPLACE_APP}
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