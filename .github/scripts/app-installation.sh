#!/usr/bin/env bash

set -e

SSH_TIMEOUT=600
DEPLOYMENT_SCRIPT="${APP_NAME#linode-marketplace-}-deploy.sh"
REMOTE_DIR="/root/deployment"

SSH_OPTS=(
  -o StrictHostKeyChecking=no
  -o ConnectTimeout=10
  -o ServerAliveInterval=30
  -o ServerAliveCountMax=10
  -o TCPKeepAlive=yes
)

wait_for_ssh() {
  local deadline=$((SECONDS + SSH_TIMEOUT))

  until sshpass -p "$LINODE_ROOT_PASS" ssh "${SSH_OPTS[@]}" "root@$LINODE_IPV4" "exit"; do
    if [ "$SECONDS" -ge "$deadline" ]; then
      echo "Timeout reached after ${SSH_TIMEOUT}s. Unable to connect to Linode via SSH."
      exit 1
    fi
    echo "Waiting for SSH to be ready... ($((deadline - SECONDS))s remaining)"
    sleep 10
  done

  echo "Connected to Linode via SSH"
}

copy_deployment_scripts() {
  echo "Copying deployment_scripts/$APP_NAME to $REMOTE_DIR"
  sshpass -p "$LINODE_ROOT_PASS" scp -r "${SSH_OPTS[@]}" \
  "deployment_scripts/$APP_NAME" \
  "root@$LINODE_IPV4:$REMOTE_DIR"
}

run_remote_deploy() {
  echo "Deploying $APP_NAME on $IMAGE image"

  set +e
  sshpass -p "$LINODE_ROOT_PASS" ssh "${SSH_OPTS[@]}" \
  "root@$LINODE_IPV4" \
  "
   export LINODE_API_SECRET=$LINODE_API_SECRET
   export GH_USER=$GH_USER
   export BRANCH=$BRANCH
   export APP_NAME=$APP_NAME
   export DEPLOYMENT_SCRIPT=$DEPLOYMENT_SCRIPT
   export HF_TOKEN=$HF_TOKEN
   export CERTBOT_TEST_CERT=--test-cert

   cd $REMOTE_DIR
   chmod +x test-vars.sh $DEPLOYMENT_SCRIPT
   . ./test-vars.sh
   ./$DEPLOYMENT_SCRIPT
   "

  local rc=$?
  set -e

  if [ "$rc" -eq 255 ]; then
    echo "SSH disconnected (exit 255). Assuming remote reboot occurred; continuing."
    rc=0
  fi

  if [ "$rc" -ne 0 ]; then
    echo "Remote deployment failed with exit code $rc"
    exit "$rc"
  fi
}

wait_for_ssh
copy_deployment_scripts
run_remote_deploy
wait_for_ssh
