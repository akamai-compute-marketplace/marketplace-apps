#!/bin/bash

set -euo pipefail

REGION="us-ord"
LINODE_TYPE="g6-dedicated-4"
IMAGE="linode/ubuntu24.04"

{
	echo "REGION=${REGION}"
	echo "LINODE_TYPE=${LINODE_TYPE}"
	echo "IMAGE=${IMAGE}"
} >>"$GITHUB_ENV"
