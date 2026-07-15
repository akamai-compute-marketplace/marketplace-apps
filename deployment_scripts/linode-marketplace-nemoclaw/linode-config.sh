#!/bin/bash

set -euo pipefail

REGION="us-east"
LINODE_TYPE="g6-standard-8"
IMAGE="linode/ubuntu24.04"

echo "REGION=${REGION}" >>"$GITHUB_ENV"
echo "LINODE_TYPE=${LINODE_TYPE}" >>"$GITHUB_ENV"
echo "IMAGE=${IMAGE}" >>"$GITHUB_ENV"
