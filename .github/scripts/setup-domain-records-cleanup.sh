#!/usr/bin/env bash

set -e

ACCEPT_HEADER="accept: application/json"
AUTH_TOKEN="Authorization: Bearer $LINODE_API_SECRET"

echo "Getting Domain id for $LINODE_DOMAIN..."

# Getting domain ID for $LINODE_DOMAIN
DOMAIN_ID=$(curl -s --request GET \
    --url https://api.linode.com/v4/domains \
    --header "$ACCEPT_HEADER" \
    --header "$AUTH_TOKEN" |
    jq -r --arg linode_domain "$LINODE_DOMAIN" '.data[] | select(.domain == $linode_domain) | .id')

if [ -z "$DOMAIN_ID" ] || [ "$DOMAIN_ID" == "null" ]; then
    echo "Domain $LINODE_DOMAIN not found. Please check if it exists in your Linode account."
    exit 1
fi

echo "Domain ID for $LINODE_DOMAIN is $DOMAIN_ID"

# Getting all records for $LINODE_DOMAIN
RECORDS_JSON=$(curl -s --request GET \
    --url "https://api.linode.com/v4/domains/$DOMAIN_ID/records" \
    --header "$ACCEPT_HEADER" \
    --header "$AUTH_TOKEN")

# Filtering records with name=$LINODE_SUBDOMAIN and getting their IDs
MATCHING_IDS=($(echo "$RECORDS_JSON" | jq -r --arg linode_subdomain "$LINODE_SUBDOMAIN" '.data[] | select(.name == $linode_subdomain) | .id'))

if [ ${#MATCHING_IDS[@]} -eq 0 ]; then
    echo "No records found for subdomain $LINODE_SUBDOMAIN. Exiting without any action."
    exit 0
fi

echo "Found ${#MATCHING_IDS[@]} record(s) with name=$LINODE_SUBDOMAIN for domain $LINODE_DOMAIN."

# Deleting each matching record
for RECORD_ID in "${MATCHING_IDS[@]}"; do
    echo "Deleting record ID $RECORD_ID with name=$LINODE_SUBDOMAIN"
    curl -s -o /dev/null -X DELETE --url "https://api.linode.com/v4/domains/$DOMAIN_ID/records/$RECORD_ID" --header "$ACCEPT_HEADER" --header "$AUTH_TOKEN"
done

echo "Domain records clean up completed."
exit 0