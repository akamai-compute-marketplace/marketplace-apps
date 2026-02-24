#!/bin/bash

set -euo pipefail

REGION="us-ord"
LINODE_TYPE="g6-dedicated-4"
IMAGE="linode/ubuntu22.04"

echo "REGION=${REGION}" >> "$GITHUB_ENV"
echo "LINODE_TYPE=${LINODE_TYPE}" >> "$GITHUB_ENV"
echo "IMAGE=${IMAGE}" >> "$GITHUB_ENV"