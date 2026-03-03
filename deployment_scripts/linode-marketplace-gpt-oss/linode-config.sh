#!/bin/bash

set -euo pipefail

REGION="us-ord"
LINODE_TYPE="g2-gpu-rtx4000a1-s"
IMAGE="linode/ubuntu24.04"

echo "REGION=${REGION}" >> "$GITHUB_ENV"
echo "LINODE_TYPE=${LINODE_TYPE}" >> "$GITHUB_ENV"
echo "IMAGE=${IMAGE}" >> "$GITHUB_ENV"
