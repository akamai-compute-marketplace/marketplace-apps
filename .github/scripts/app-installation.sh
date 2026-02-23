#!/usr/bin/env bash

set -e

SSH_TIMEOUT=600
DEPLOYMENT_SCRIPT="${APP_NAME#linode-marketplace-}-deploy.sh"

wait_for_ssh() {
  local timeout="${1:-$SSH_TIMEOUT}"
  local elapsed=0

  while true; do
    if sshpass -p "$LINODE_ROOT_PASS" ssh -o StrictHostKeyChecking=accept-new root@"$LINODE_IPV4" "exit"; then
      echo "Connected to Linode via SSH"
      break
    fi
    if [ "$elapsed" -ge "$timeout" ]; then
      echo "Timeout reached. Unable to connect to Linode via SSH."
      exit 1
    fi
    echo "Waiting for SSH to be ready... (${elapsed}s/${timeout}s)"
    sleep 10
    elapsed=$((elapsed + 10))
  done
}

ubuntu_deploy() {
  set +e
  sshpass -p "$LINODE_ROOT_PASS" ssh \
  -o StrictHostKeyChecking=no \
  -o ServerAliveInterval=30 \
  -o ServerAliveCountMax=10 \
  -o TCPKeepAlive=yes \
  root@"$LINODE_IPV4" \
  "export LINODE_API_SECRET='$LINODE_API_SECRET'; \
   export LINODE_DOMAIN='$LINODE_DOMAIN'; \
   export GH_USER='$GH_USER'; \
   export BRANCH='$BRANCH'; \
   export GIT_REPO='$GIT_REPO'; \
   export APP_NAME='$APP_NAME'; \
   export DEPLOYMENT_SCRIPT='$DEPLOYMENT_SCRIPT'; \
   export HF_TOKEN='$HF_TOKEN'; \
   git clone --depth 1 --branch \"\$BRANCH\" \"\$GIT_REPO\" /root/repo; \
   cd /root/repo/deployment_scripts/\"\$APP_NAME\"; \
   chmod +x test-vars.sh \"\$DEPLOYMENT_SCRIPT\"; \
   . ./test-vars.sh; \
   ./\"\$DEPLOYMENT_SCRIPT\""

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

almalinux_deploy() {
  sshpass -p "$LINODE_ROOT_PASS" ssh \
    -o StrictHostKeyChecking=no \
    -o ServerAliveInterval=30 \
    -o ServerAliveCountMax=10 \
    -o TCPKeepAlive=yes \
    root@"$LINODE_IPV4" \
    "export LINODE_API_SECRET='${LINODE_API_SECRET}'; \
     export LINODE_DOMAIN='${LINODE_DOMAIN}'; \
     export GH_USER='${GH_USER}'; \
     export BRANCH='${BRANCH}'; \
     export GIT_REPO='${GIT_REPO}'; \
     export APP_NAME='${APP_NAME}'; \
     export DEPLOYMENT_SCRIPT='${DEPLOYMENT_SCRIPT}'; \
     dnf -y install git; \
     git clone --depth 1 --branch \"\$BRANCH\" \"\$GIT_REPO\" /root/repo; \
     cd \"/root/repo/deployment_scripts/\$APP_NAME\"; \
     chmod +x test-vars.sh \"\$DEPLOYMENT_SCRIPT\"; \
     . ./test-vars.sh; \
     ./\"\$DEPLOYMENT_SCRIPT\""
}

run_remote_deploy() {
  if [[ "$IMAGE" == *"ubuntu"* ]]; then
    echo "Detected Ubuntu image"
    ubuntu_deploy
  elif [[ "$IMAGE" == *"almalinux"* ]]; then
    echo "Detected AlmaLinux image"
    almalinux_deploy
  else
    echo "Unsupported image distribution: $IMAGE" >&2
    exit 1
  fi
}

wait_for_ssh
run_remote_deploy
wait_for_ssh

