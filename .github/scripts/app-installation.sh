#!/usr/bin/env bash

set -e

SSH_TIMEOUT=300
SSH_ELAPSED=0
DEPLOYMENT_SCRIPT="${APP_NAME#linode-marketplace-}-deploy.sh"

while true; do
	if sshpass -p $LINODE_ROOT_PASS ssh -o StrictHostKeyChecking=accept-new root@$LINODE_IPV4 "exit"; then
		break
	fi
	if [ "$SSH_ELAPSED" -ge "$SSH_TIMEOUT" ]; then
		echo "Timeout reached. Unable to connect to Linode via SSH."
		exit 1
	fi
	echo "Waiting for SSH to be ready..."
	sleep 10
	SSH_ELAPSED=$((SSH_ELAPSED + 10))
done

sshpass -p "$LINODE_ROOT_PASS" ssh -o StrictHostKeyChecking=no root@"$LINODE_IPV4" "
  git clone --depth 1 --branch \"${GITHUB_HEAD_REF}\" \"${GITHUB_CLONE_URL}\" /root/repo &&
  cd /root/repo/deployment_scripts/\"$APP_NAME\" &&
  chmod +x test-vars.sh $DEPLOYMENT_SCRIPT &&
  . ./test-vars.sh &&
  ./$DEPLOYMENT_SCRIPT
"
