#!/bin/bash
# CI infrastructure config for discourse. Exports the Linode spec to $GITHUB_ENV.

set -euo pipefail

REGION="us-east"
LINODE_TYPE="g6-standard-2"
IMAGE="linode/ubuntu24.04"

{
	echo "REGION=${REGION}"
	echo "LINODE_TYPE=${LINODE_TYPE}"
	echo "IMAGE=${IMAGE}"
} >>"$GITHUB_ENV"
