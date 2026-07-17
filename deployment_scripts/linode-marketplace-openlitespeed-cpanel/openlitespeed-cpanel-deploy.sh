#!/bin/bash
# STACKSCRIPT_ID: TBD
# enable logging
exec > >(tee /dev/ttyS0 /var/log/stackscript.log) 2>&1

## Linode/SSH security settings
#<UDF name="user_name" label="The limited sudo user to be created for the Linode: *No Capital Letters or Special Characters*">

# BEGIN CI-MODE
#DEBUG="NO"
if [[ -n ${DEBUG} ]]; then
	if [ "${DEBUG}" == "NO" ]; then
		trap "cleanup $? $LINENO" EXIT
	fi
else
	trap "cleanup $? $LINENO" EXIT
fi

# cleanup will always happen. If DEBUG is passed and is anything
# other than NO, it will always trigger cleanup. This is useful for
# ci testing and passing vars to the instance.

if [ "${MODE}" == "staging" ]; then
	trap "provision_failed $? $LINENO" ERR
else
	set -e
fi
# END CI-MODE

# BEGIN CI-GH
if [[ -n ${GH_USER} && -n ${BRANCH} ]]; then
	echo "[info] git user and branch set.."
	export GIT_REPO="https://github.com/${GH_USER}/marketplace-apps.git"

else
	export GH_USER="akamai-compute-marketplace"
	export BRANCH="main"
	export GIT_REPO="https://github.com/${GH_USER}/marketplace-apps.git"
fi
# END CI-GH

export WORK_DIR="/root/marketplace-apps"
export MARKETPLACE_APP="apps/linode-marketplace-openlitespeed-cpanel"

# BEGIN CI-PROVISION-FUNC
function provision_failed {
	echo "[info] Provision failed. Sending status.."

	# dep
	dnf install jq -y

	# set token
	local token=($(curl -ks -X POST ${KC_SERVER} \
		-H "Content-Type: application/json" \
		-d "{ \"username\":\"${KC_USERNAME}\", \"password\":\"${KC_PASSWORD}\" }" | jq -r .token))

	# send pre-provision failure
	curl -sk -X POST ${DATA_ENDPOINT} \
		-H "Authorization: ${token}" \
		-H "Content-Type: application/json" \
		-d "{ \"app_label\":\"${APP_LABEL}\", \"status\":\"provision_failed\", \"branch\": \"${BRANCH}\", \
        \"gituser\": \"${GH_USER}\", \"runjob\": \"${RUNJOB}\", \"image\":\"${IMAGE}\", \
        \"type\":\"${TYPE}\", \"region\":\"${REGION}\", \"instance_env\":\"${INSTANCE_ENV}\" }"

	exit $?
}
# END CI-PROVISION-FUNC

function cleanup {
	if [ -d "${WORK_DIR}" ]; then
		rm -rf ${WORK_DIR}
	fi
}

function run {
	dnf update -y
	dnf install -y git python3 python3-pip
	dnf makecache
	dnf install -y epel-release
	dnf makecache
}

function udf {
	local group_vars="${WORK_DIR}/${MARKETPLACE_APP}/group_vars/linode/vars"
	echo "username: ${USER_NAME}" >>${group_vars}
	echo "default_dns: $(hostname -I | awk '{print $1}' | tr '.' '-' | awk '{print $1 ".ip.linodeusercontent.com"}')" >>${group_vars}

	# BEGIN CI-UDF-CI-MODE
	# staging or production mode (ci)
	if [[ "${MODE}" == "staging" ]]; then
		echo "[info] running in staging mode..."
		echo "mode: ${MODE}" >>${group_vars}
	else
		echo "[info] running in production mode..."
		echo "mode: production" >>${group_vars}
	fi
	# END CI-UDF-CI-MODE
}

function final_run {
	# clone repo and set up ansible environment
	git -C /root clone -b ${BRANCH} ${GIT_REPO}

	# venv
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
	echo "Installation complete. WHM: https://$(hostname -I | awk '{print $1}'):2087 LiteSpeed WebAdmin credentials: /root/.credentials"
}

# main
run
final_run
installation_complete
