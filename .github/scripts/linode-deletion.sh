#!/usr/bin/env bash

set -e

if [ -n "$LINODE_ID" ] && [ "$LINODE_ID" != "null" ]; then
	RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE \
		-H "Authorization: Bearer $LINODE_API_SECRET" \
		https://api.linode.com/v4/linode/instances/$LINODE_ID)
	if [ "$RESPONSE" = "200" ]; then
		echo "Linode $LINODE_ID deleted successfully."
	else
		echo "Failed to delete Linode $LINODE_ID. Status code: $RESPONSE"
		exit 1
	fi
else
	echo "No Linode ID found to delete."
fi
