#!/bin/bash
# STACKSCRIPT_ID: 688891

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

# <UDF name="user_name" label="The limited sudo user to be created for the Linode: *No Capital Letters or Special Characters*">
# <UDF name="disable_root" label="Disable root access over SSH?" oneOf="Yes,No" default="No">

## Domain Settings
# <UDF name="token_password" label="Your Linode API token. This is needed to create your server's DNS records" default="">
# <UDF name="subdomain" label="Subdomain" example="The subdomain for the DNS record: www (Requires Domain)" default="">
# <UDF name="domain" label="Domain" example="The domain for the DNS record: example.com (Requires API token)" default="">

## Discourse Settings
# <UDF name="admin_email" label="Admin email address (becomes the Discourse admin account's login)" example="admin@example.com">
# <UDF name="smtp_address" label="SMTP server address (optional - required for Discourse to send email)" example="smtp.mailgun.org" default="">
# <UDF name="smtp_port" label="SMTP port" example="587" default="587">
# <UDF name="smtp_user_name" label="SMTP username" default="">
# <UDF name="smtp_password" label="SMTP password" default="">
# <UDF name="smtp_notification_email" label="Dicourse notification email" default="">

## Addons
# <UDF name="add_ons" label="Optional data exporter Add-ons for your deployment" manyOf="node_exporter,mysqld_exporter,newrelic,none" default="none">

#GH_USER=""
#BRANCH=""

if [[ -n ${GH_USER} && -n ${BRANCH} ]]; then
	echo "[info] git user and branch set.."
	export GIT_REPO="https://github.com/${GH_USER}/marketplace-apps.git"
else
	export GH_USER="akamai-compute-marketplace"
	export BRANCH="main"
	export GIT_REPO="https://github.com/${GH_USER}/marketplace-apps.git"
fi

export WORK_DIR="/tmp/marketplace-apps"
export MARKETPLACE_APP="apps/linode-marketplace-discourse"
export DEBIAN_FRONTEND=noninteractive

function cleanup {
	if [ -d "${WORK_DIR}" ]; then 
	  rm -rf "${WORK_DIR}"
	fi
}

function udf {
	local group_vars="${WORK_DIR}/${MARKETPLACE_APP}/group_vars/linode/vars"
	sed 's/  //g' <<EOF > ${group_vars}
# sudo username
username: ${USER_NAME}

# smtp vars
admin_email: ${ADMIN_EMAIL}
smtp_address: ${SMTP_ADDRESS}
smtp_user_name: ${SMTP_USER_NAME}
smtp_port: ${SMTP_PORT}
smtp_password: ${SMTP_PASSWORD}
smtp_notification_email: $SMTP_NOTIFICATION_EMAIL}

# addons
add_ons: [${ADD_ONS}]
EOF

	if [ "$DISABLE_ROOT" = "Yes" ]; then
    	echo "disable_root: yes" >> ${group_vars};
  	else echo "Leaving root login enabled";
  	fi

	if [[ -n ${DOMAIN} ]]; then
		echo "domain: ${DOMAIN}" >>"${group_vars}"
	else
		echo "default_dns: $(hostname -I | awk '{print $1}' | tr '.' '-' | awk '{print $1 ".ip.linodeusercontent.com"}')" >>"${group_vars}"
	fi

  	if [[ -n ${SUBDOMAIN} ]]; then
  	  echo "subdomain: ${SUBDOMAIN}" >> ${group_vars}
  	else echo "subdomain: www" >> ${group_vars}
  	fi

  	if [[ -n ${TOKEN_PASSWORD} ]]; then
  	  echo "token_password: ${TOKEN_PASSWORD}" >> ${group_vars}
  	else echo "No API token entered";
  	fi
}

function run {
	apt-get update
	apt-get install -y git python3 python3-pip python3-venv
	git -C /tmp clone -b "${BRANCH}" "${GIT_REPO}"
	cd "${WORK_DIR}/${MARKETPLACE_APP}"
	python3 -m venv env
	source env/bin/activate
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

run
installation_complete