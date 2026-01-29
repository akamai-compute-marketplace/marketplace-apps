#!/usr/bin/env bash

set -e

TIMEOUT=300
ELAPSED=0

RESPONSE=$(curl -s -o response.json -w "%{http_code}" \
	-H "Content-Type: application/json" \
	-H "Authorization: Bearer $LINODE_API_SECRET" \
	-X POST -d "{
                \"image\": \"linode/ubuntu22.04\",
                \"maintenance_policy\": \"linode/migrate\",
                \"private_ip\": false,
                \"region\": \"${REGION}\",
                \"type\": \"${LINODE_TYPE}\",
                \"label\": \"ubuntu-${APP_NAME}\",
                \"root_pass\": \"$LINODE_ROOT_PASS\",
                \"disk_encryption\": \"enabled\"
            }" https://api.linode.com/v4/linode/instances)

if [ "$RESPONSE" -ne 200 ]; then
	echo "API call failed with status code $RESPONSE"
	jq '{errors}' response.json
	exit 1
fi

LINODE_ID=$(jq -r '.id' response.json)
echo "LINODE_ID=$LINODE_ID" >>$GITHUB_OUTPUT

LINODE_IPV4=$(jq -r '.ipv4[0]' response.json)
echo "::add-mask::$LINODE_IPV4"
echo "LINODE_IPV4=$LINODE_IPV4" >>$GITHUB_OUTPUT

while true; do
	STATUS=$(curl -s -H "Authorization: Bearer $LINODE_API_SECRET" \
		https://api.linode.com/v4/linode/instances/$LINODE_ID | jq -r '.status')
	echo "Current Linode status: $STATUS"
	if [ "$STATUS" == "running" ]; then
		break
	fi
	if [ "$ELAPSED" -ge "$TIMEOUT" ]; then
		echo "Timeout reached. Linode provisioning failed."
		exit 1
	fi
	echo "Waiting for Linode to be provisioned..."
	sleep 10
	ELAPSED=$((ELAPSED + 10))
done
