#!/bin/bash

set -euo pipefail

# What Akamai's CI deploys the app on (as other apps' linode-config.sh): Ubuntu 24.04, and a
# 2-core shared plan, enough for a few lives; customers pick their own size.
REGION="us-ord"
LINODE_TYPE="g6-standard-2"
IMAGE="linode/ubuntu24.04"

echo "REGION=${REGION}" >> "$GITHUB_ENV"
echo "LINODE_TYPE=${LINODE_TYPE}" >> "$GITHUB_ENV"
echo "IMAGE=${IMAGE}" >> "$GITHUB_ENV"
