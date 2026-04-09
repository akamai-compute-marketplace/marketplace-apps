#!/bin/bash
# ==============================================================================
# rtSurvey - Linode Marketplace StackScript
# ==============================================================================
# Thin bootstrap: installs Ansible, clones the rtSurvey Ansible playbook repo,
# then runs site.yml to do the full deployment.
#
# All real deployment logic lives in:
#   https://github.com/therealtimex/rtsurvey-linode-marketplace
# ==============================================================================

# <UDF name="sudo_username" label="Limited Sudo Username" example="rtuser" />
# <UDF name="sudo_password" label="Limited Sudo User Password" example="s3cur3P@ss" />
# <UDF name="ssh_public_key" label="SSH Public Key" example="ssh-rsa AAAA..." default="" />
# <UDF name="timezone" label="Timezone" example="Asia/Ho_Chi_Minh" default="Asia/Ho_Chi_Minh" />

set -euo pipefail
exec > >(tee /dev/ttyS0 /var/log/stackscript.log) 2>&1
trap 'echo "ERROR: StackScript failed at line $LINENO (exit $?)" >&2' ERR

# Linode injects UDF values as UPPERCASE environment variables
# e.g. name="sudo_username" becomes $SUDO_USERNAME
SUDO_USERNAME="${SUDO_USERNAME:-}"
SUDO_PASSWORD="${SUDO_PASSWORD:-}"
SSH_PUBLIC_KEY="${SSH_PUBLIC_KEY:-}"
TZ_VALUE="${TIMEZONE:-Asia/Ho_Chi_Minh}"

# Validate required UDFs
[[ -n "${SUDO_USERNAME}" ]] || { echo "ERROR: SUDO_USERNAME UDF is required"; exit 1; }
[[ -n "${SUDO_PASSWORD}" ]] || { echo "ERROR: SUDO_PASSWORD UDF is required"; exit 1; }

WORK_DIR="/tmp/marketplace-deploy"
ANSIBLE_REPO="https://github.com/therealtimex/rtsurvey-linode-marketplace.git"
ANSIBLE_BRANCH="main"

echo "============================================================"
echo " rtSurvey Marketplace StackScript - $(date)"
echo "============================================================"

# ------------------------------------------------------------------------------
# 1. System update + Python + pip
# ------------------------------------------------------------------------------
echo "[1/4] Updating system and installing Python..."
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq git python3-pip python3-venv

# ------------------------------------------------------------------------------
# 2. Bootstrap Ansible in a venv
# ------------------------------------------------------------------------------
echo "[2/4] Installing Ansible..."
mkdir -p "${WORK_DIR}"
python3 -m venv "${WORK_DIR}/venv"
# shellcheck disable=SC1091
source "${WORK_DIR}/venv/bin/activate"

pip install -q --upgrade pip

# ------------------------------------------------------------------------------
# 3. Clone Ansible playbook repo
# ------------------------------------------------------------------------------
echo "[3/4] Cloning rtSurvey Ansible playbook repo..."
git clone --depth=1 --branch "${ANSIBLE_BRANCH}" "${ANSIBLE_REPO}" "${WORK_DIR}/app"
cd "${WORK_DIR}/app"

# Install Python dependencies (pins ansible + jinja2 versions)
pip install -q -r requirements.txt

# Install Ansible collections
ansible-galaxy collection install -r collections.yml --timeout 60

# ------------------------------------------------------------------------------
# 4. Run Ansible playbook
# ------------------------------------------------------------------------------
echo "[4/4] Running Ansible playbook..."
ansible-playbook site.yml \
  -e "sudo_username=${SUDO_USERNAME}" \
  -e "sudo_password=${SUDO_PASSWORD}" \
  -e "ssh_public_key=${SSH_PUBLIC_KEY}" \
  -e "tz=${TZ_VALUE}"

# ------------------------------------------------------------------------------
# Cleanup
# ------------------------------------------------------------------------------
deactivate
rm -rf "${WORK_DIR}"

echo "============================================================"
echo " rtSurvey deployment complete!"
echo " See /var/log/stackscript.log for full log"
echo "============================================================"
