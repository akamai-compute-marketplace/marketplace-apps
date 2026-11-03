#!/bin/bash
# STACKSCRIPT_ID: 2260640

# enable logging
set -e
exec > >(tee /dev/ttyS0 /var/log/stackscript.log) 2>&1

#DEBUG="NO"
# cleanup will always happen. If DEBUG is passed and is anything
# other than NO, it will always trigger cleanup. This is useful for
# ci testing and passing vars to the instance.

if [[ -n ${DEBUG} ]]; then
  if [ "${DEBUG}" == "NO" ]; then
    trap "cleanup $? $LINENO" EXIT
  fi
else
  trap "cleanup $? $LINENO" EXIT
fi

## Linode/SSH security settings
#<UDF name="user_name" label="The limited sudo user to be created for the Linode: *No Capital Letters or Special Characters*">
#<UDF name="disable_root" label="Disable root access over SSH?" oneOf="Yes,No" default="No">

## Domain Settings
#<UDF name="token_password" label="Your Linode API token. This is needed to create your server's DNS records" default="">
#<UDF name="subdomain" label="Subdomain" example="The subdomain for the DNS record: www (Requires Domain)" default="">
#<UDF name="domain" label="Domain" example="The domain for the DNS record: example.com (Requires API token)" default="">

## Coolify setup
#<UDF name="soa_email_address" label="Email address (used for the SSL certificate and your Coolify login)" example="user@domain.tld">

## Addons
#<UDF name="add_ons" label="Optional data exporter Add-ons for your deployment" manyOf="node_exporter,mysqld_exporter,newrelic,none" default="none">


if [[ -n ${GH_USER} && -n ${BRANCH} ]]; then
	echo "[info] git user and branch set.."
else
	export GH_USER="akamai-compute-marketplace"
	export BRANCH="main"
fi
export GIT_REPO="https://github.com/${GH_USER}/marketplace-apps.git"

export WORK_DIR="/tmp/marketplace-apps"
export MARKETPLACE_APP="apps/linode-marketplace-coolify"

function cleanup {
	if [ -d "${WORK_DIR}" ]; then
		rm -rf ${WORK_DIR}
	fi
}

function udf {
	local group_vars="${WORK_DIR}/${MARKETPLACE_APP}/group_vars/linode/vars"
	sed 's/  //g' <<EOF >${group_vars}
  # sudo username
  username: ${USER_NAME}
  soa_email_address: ${SOA_EMAIL_ADDRESS}
  # addons
  add_ons: [${ADD_ONS}]
EOF

	if [ "$DISABLE_ROOT" = "Yes" ]; then
		echo "disable_root: yes" >>${group_vars}
	else
		echo "Leaving root login enabled"
	fi

	if [[ -n ${DOMAIN} ]]; then
		echo "domain: ${DOMAIN}" >>${group_vars}
	else
		echo "default_dns: $(hostname -I | awk '{print $1}' | tr '.' '-' | awk '{print $1 ".ip.linodeusercontent.com"}')" >>${group_vars}
	fi

	if [[ -n ${SUBDOMAIN} ]]; then
		echo "subdomain: ${SUBDOMAIN}" >>${group_vars}
	else
		echo "subdomain: www" >>${group_vars}
	fi

	if [[ -n ${TOKEN_PASSWORD} ]]; then
		echo "token_password: ${TOKEN_PASSWORD}" >>${group_vars}
	else
		echo "No API token entered"
	fi
}

function run {
	# install dependencies
	apt-get update
	apt-get install -y git python3 python3-pip python3-venv

	# clone the repo and set up ansible
	git -C /tmp clone --recurse-submodules -b ${BRANCH} ${GIT_REPO}
	cd ${WORK_DIR}/${MARKETPLACE_APP}
	python3 -m venv env
	source env/bin/activate
	pip install pip --upgrade
	pip install -r requirements.txt
	ansible-galaxy install -r collections.yml

	udf
	ansible-playbook -v provision.yml && ansible-playbook -v site.yml
}

run
echo "Installation Complete"
